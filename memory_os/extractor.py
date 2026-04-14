"""Schema-driven extraction pipeline (phase-1 skeleton)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ExtractionResult:
    structured_memory: Dict[str, Any]
    validation_hints: List[str]


IGNORED_FIELDS = {"x", "y", "export", "non_design_metadata"}


def normalize_node(node: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {k: v for k, v in node.items() if k not in IGNORED_FIELDS}
    normalized.setdefault("hierarchy", {"childCount": len(normalized.get("children", []))})
    normalized.setdefault("autoLayout", {"enabled": False})
    normalized.setdefault(
        "componentSemantics",
        {"component": False, "variant": False, "instance": False, "reference": None, "variantProperties": None},
    )
    normalized.setdefault("tokens", {"color": [], "typography": [], "effect": []})

    if "children" in normalized:
        normalized["children"] = [normalize_node(child) for child in normalized["children"]]
        normalized["hierarchy"]["childCount"] = len(normalized["children"])

    return normalized


def extract_by_schema(nodes: List[Dict[str, Any]]) -> ExtractionResult:
    structured = {"schemaVersion": "component@1.0.0", "nodes": [normalize_node(node) for node in nodes]}
    hints: List[str] = []

    for node in structured["nodes"]:
        if node.get("autoLayout", {}).get("enabled") and not node["tokens"]["color"]:
            hints.append(f"node:{node.get('id')} missing color token reference")

    return ExtractionResult(structured_memory=structured, validation_hints=hints)
