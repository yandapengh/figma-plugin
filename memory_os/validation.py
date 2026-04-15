"""Validation pipeline for schema/rule/write minimal gate layers."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Set

MODE = "annotation_user_controlled_minimal_gate@1.0.0"
VALID_AUTO_LAYOUT_DIRECTIONS = {"HORIZONTAL", "VERTICAL"}
NODE_LINKED_MAPPING_KEY = "nodeId"


def _is_json_serializable(payload: Any) -> bool:
    try:
        json.dumps(payload)
    except (TypeError, ValueError):
        return False
    return True


def validate_schema(memory: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    nodes = memory.get("nodes")
    if nodes is None:
        errors.append("schema:nodes_missing")
        return errors

    if not isinstance(nodes, list):
        errors.append("schema:nodes_not_list")
        return errors

    for idx, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"schema:node_not_object:{idx}")
            continue

        if "id" not in node or node.get("id") in (None, ""):
            errors.append(f"schema:node_id_missing:{idx}")

        auto = node.get("autoLayout")
        if auto is not None and not isinstance(auto, dict):
            errors.append(f"schema:autoLayout_not_object:{node.get('id', idx)}")

    return errors


def validate_rules(memory: Dict[str, Any]) -> List[str]:
    warnings: List[str] = []

    for node in memory.get("nodes", []):
        if not isinstance(node, dict):
            continue

        auto = node.get("autoLayout")
        if not isinstance(auto, dict):
            continue

        enabled = bool(auto.get("enabled"))
        direction = auto.get("direction")
        node_id = node.get("id")

        # 合同校验：enabled=true 且缺失 direction，降级 warning（保留用户控制优先）。
        if enabled and direction is None:
            warnings.append(f"rule:direction_missing:{node_id}")
            continue

        # 枚举校验：direction 非法，默认 warning 不阻断。
        if enabled and direction not in VALID_AUTO_LAYOUT_DIRECTIONS:
            warnings.append(f"rule:invalid_direction:{node_id}")

    return warnings


def _collect_node_linked_write_errors(payload: Dict[str, Any], errors: List[str]) -> None:
    notes = payload.get("notes")
    if isinstance(notes, list):
        for idx, note in enumerate(notes):
            if not isinstance(note, dict):
                errors.append(f"write:note_not_object:{idx}")
                continue

            if note.get("nodeLinked") or note.get("node_linked"):
                if note.get(NODE_LINKED_MAPPING_KEY) in (None, ""):
                    errors.append(f"write:node_link_missing_nodeId:{idx}")

    if payload.get("nodeLinked") or payload.get("node_linked"):
        if payload.get(NODE_LINKED_MAPPING_KEY) in (None, ""):
            errors.append("write:node_link_missing_nodeId")


def write_payload_validation(write_payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    if not _is_json_serializable(write_payload):
        errors.append("write:payload_not_serializable")
        return errors

    if write_payload.get("schemaVersion") in (None, "") and write_payload.get("schema_version") in (None, ""):
        errors.append("write:schema_version_missing")

    _collect_node_linked_write_errors(write_payload, errors)

    return errors


def _node_map(memory: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    nodes = memory.get("nodes", [])
    if not isinstance(nodes, list):
        return {}
    return {
        str(node.get("id")): node
        for node in nodes
        if isinstance(node, dict) and node.get("id") not in (None, "")
    }


def detect_structure_change_type(
    previous_memory: Optional[Dict[str, Any]],
    current_memory: Dict[str, Any],
) -> List[str]:
    """Detect structure change categories between two memory snapshots."""

    if not isinstance(previous_memory, dict):
        return ["additive"]

    previous_nodes = _node_map(previous_memory)
    current_nodes = _node_map(current_memory)

    if not previous_nodes and current_nodes:
        return ["additive"]

    detected: Set[str] = set()

    prev_ids = set(previous_nodes.keys())
    curr_ids = set(current_nodes.keys())

    if curr_ids - prev_ids:
        detected.add("additive")

    if prev_ids - curr_ids:
        detected.add("delete")

    for node_id in prev_ids & curr_ids:
        previous_node = previous_nodes[node_id]
        current_node = current_nodes[node_id]

        if previous_node.get("parentId") != current_node.get("parentId"):
            detected.add("move")

        previous_name = previous_node.get("name") or previous_node.get("title")
        current_name = current_node.get("name") or current_node.get("title")
        if previous_name is not None and current_name is not None and previous_name != current_name:
            detected.add("rename")

    if any(
        isinstance(node, dict) and bool(node.get("_restructure") or node.get("restructure"))
        for node in current_memory.get("nodes", [])
    ):
        detected.add("restructure")

    if not detected:
        return ["additive"]

    return sorted(detected)


def validate_structure_changes(
    structure_change_types: List[str],
    *,
    restructure_mode: bool = False,
    restructure_confirmed: bool = False,
) -> List[str]:
    """Block all non-additive structure changes by default."""

    errors: List[str] = []
    for change_type in structure_change_types:
        if change_type == "additive":
            continue
        if change_type == "restructure" and restructure_mode and restructure_confirmed:
            continue
        errors.append(f"structure:blocked:{change_type}")
    return errors


def validate_pipeline(
    memory: Dict[str, Any],
    write_payload: Optional[Dict[str, Any]] = None,
    *,
    previous_memory: Optional[Dict[str, Any]] = None,
    restructure_mode: bool = False,
    restructure_confirmed: bool = False,
) -> Dict[str, Any]:
    schema_errors = validate_schema(memory)
    rule_warnings = validate_rules(memory)

    payload = write_payload if isinstance(write_payload, dict) else memory
    write_errors = write_payload_validation(payload)

    structure_change_types = detect_structure_change_type(previous_memory, memory)
    structure_change_errors = validate_structure_changes(
        structure_change_types,
        restructure_mode=restructure_mode,
        restructure_confirmed=restructure_confirmed,
    )

    return {
        "pass": len(schema_errors) == 0 and len(write_errors) == 0 and len(structure_change_errors) == 0,
        "schema_errors": schema_errors,
        "rule_warnings": rule_warnings,
        "write_errors": write_errors,
        "structure_change_errors": structure_change_errors,
        "structure_change_types": structure_change_types,
        "mode": MODE,
    }
