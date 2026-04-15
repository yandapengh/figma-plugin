"""Structure-change detection and validation helpers."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

VALID_STRUCTURE_CHANGE_TYPES = {"additive", "move", "rename", "delete", "restructure"}
DEFAULT_ALLOWED_STRUCTURE_CHANGE_TYPES = {"additive"}
STRUCTURE_HINT_KEYS = {
    "move": {"moved_nodes", "move_ops", "move_operations"},
    "rename": {"renamed_nodes", "rename_ops", "rename_operations"},
    "delete": {"deleted_nodes", "delete_ops", "delete_operations"},
    "restructure": {"restructure_plan", "restructure_ops", "restructure_operations"},
}


def extract_structure_change_types(payload: Dict[str, Any]) -> List[str]:
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
        inferred = infer_structure_change_types(payload)
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


def infer_structure_change_types(payload: Dict[str, Any]) -> List[str]:
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


def merge_structure_change_types(explicit_types: List[str], detected_types: List[str]) -> List[str]:
    ordered: List[str] = []
    seen = set()
    for item in explicit_types + detected_types:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered or ["additive"]
