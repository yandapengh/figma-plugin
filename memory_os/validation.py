"""Validation pipeline for schema/rule/write minimal gate layers."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from memory_os.structure_guard import (
    detect_structure_change_type,
    extract_structure_change_types,
    merge_structure_change_types,
    validate_structure_changes,
)

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
    explicit_types = extract_structure_change_types(payload)
    detected_types = detect_structure_change_type(previous_memory, memory)
    structure_change_types = merge_structure_change_types(explicit_types, detected_types)
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
