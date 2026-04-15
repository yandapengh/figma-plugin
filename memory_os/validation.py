"""Validation pipeline for schema/rule/write minimal gate layers."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Set

MODE = "annotation_user_controlled_minimal_gate@1.0.0"
VALID_AUTO_LAYOUT_DIRECTIONS = {"HORIZONTAL", "VERTICAL"}
NODE_LINKED_MAPPING_KEY = "nodeId"
VALID_STRUCTURE_CHANGE_TYPES = {"additive", "move", "rename", "delete", "restructure"}
DEFAULT_ALLOWED_STRUCTURE_CHANGE_TYPES = {"additive"}
STRUCTURE_HINT_KEYS = {
    "move": {"moved_nodes", "move_ops", "move_operations"},
    "rename": {"renamed_nodes", "rename_ops", "rename_operations"},
    "delete": {"deleted_nodes", "delete_ops", "delete_operations"},
    "restructure": {"restructure_plan", "restructure_ops", "restructure_operations"},
}


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


def _extract_structure_change_types(payload: Dict[str, Any]) -> List[str]:
    """Extract declared structure change types from payload, defaulting to additive."""

    collected: List[str] = []

    single = payload.get("structure_change_type", payload.get("structureChangeType"))
    if isinstance(single, str) and single.strip():
        collected.append(single.strip().lower())

    changes = payload.get("structure_changes", payload.get("structureChanges"))
    if isinstance(changes, list):
        for item in changes:
            if isinstance(item, str) and item.strip():
                collected.append(item.strip().lower())
                continue

            if isinstance(item, dict):
                change_type = item.get("type")
                if isinstance(change_type, str) and change_type.strip():
                    collected.append(change_type.strip().lower())

    if not collected:
        inferred = _infer_structure_change_types(payload)
        if inferred:
            collected.extend(inferred)

    if not collected:
        return ["additive"]

    deduped: List[str] = []
    seen = set()
    for value in collected:
        if value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


def _infer_structure_change_types(payload: Dict[str, Any]) -> List[str]:
    """Infer structural change types from common operation keys when explicit type is missing."""

    inferred: List[str] = []
    for change_type, keys in STRUCTURE_HINT_KEYS.items():
        for key in keys:
            value = payload.get(key)
            if value is None:
                continue
            if isinstance(value, (list, dict, tuple, set)) and len(value) == 0:
                continue
            inferred.append(change_type)
            break

    return inferred


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
        if change_type not in VALID_STRUCTURE_CHANGE_TYPES:
            errors.append(f"structure:unknown:{change_type}")
            continue
        if change_type in DEFAULT_ALLOWED_STRUCTURE_CHANGE_TYPES:
            continue
        if change_type == "restructure" and restructure_mode and restructure_confirmed:
            continue
        errors.append(f"structure:blocked:{change_type}")
    return errors


def _merge_structure_change_types(explicit_types: List[str], detected_types: List[str]) -> List[str]:
    ordered: List[str] = []
    seen = set()
    for item in explicit_types + detected_types:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered or ["additive"]


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
    explicit_types = _extract_structure_change_types(payload)
    detected_types = detect_structure_change_type(previous_memory, memory)
    structure_change_types = _merge_structure_change_types(explicit_types, detected_types)
    structure_change_errors = validate_structure_changes(
        structure_change_types,
        restructure_mode=restructure_mode or bool(payload.get("restructure_mode")),
        restructure_confirmed=restructure_confirmed or bool(payload.get("restructure_confirmed")),
    )

    return {
        "pass": len(schema_errors) == 0 and len(write_errors) == 0 and len(structure_change_errors) == 0,
        "schema_errors": schema_errors,
        "rule_warnings": rule_warnings,
        "write_errors": write_errors,
        "structure_change_types": structure_change_types,
        "structure_change_errors": structure_change_errors,
        "mode": MODE,
    }
