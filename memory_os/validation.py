"""Validation pipeline for schema/rule/generation/diff/semantic layers."""

from __future__ import annotations

from typing import Any, Dict, List


def validate_schema(memory: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if "nodes" not in memory:
        errors.append("schema:nodes_missing")
    return errors


def validate_rules(memory: Dict[str, Any]) -> List[str]:
    warnings: List[str] = []
    for node in memory.get("nodes", []):
        auto = node.get("autoLayout", {})
        if auto.get("enabled") and auto.get("direction") not in {"HORIZONTAL", "VERTICAL"}:
            warnings.append(f"rule:invalid_direction:{node.get('id')}")
    return warnings


def validate_pipeline(memory: Dict[str, Any]) -> Dict[str, Any]:
    schema_errors = validate_schema(memory)
    rule_warnings = validate_rules(memory)
    return {
        "pass": len(schema_errors) == 0,
        "schema_errors": schema_errors,
        "rule_warnings": rule_warnings,
        "generation_validation": "pending_openpencil",
        "diff_validation": "pending_openpencil",
        "llm_judge": "pending"
    }
