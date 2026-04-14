"""Human-in-the-loop decision gate: never persist without explicit approval."""

from __future__ import annotations

from typing import Any, Dict


def build_decision_payload(case_type: str, delta: Dict[str, Any], validation_report: Dict[str, Any]) -> Dict[str, Any]:
    if case_type not in {"similar_page", "new_page"}:
        raise ValueError("case_type must be similar_page or new_page")

    return {
        "case": case_type,
        "validation": validation_report,
        "delta": delta,
        "allowed_actions": (
            ["extend_existing", "fork_new_version", "reject"]
            if case_type == "similar_page"
            else ["create_new", "create_as_draft", "reject"]
        ),
        "write_allowed": False,
        "requires_user_confirmation": True,
    }


def can_persist(user_action: str, validation_passed: bool) -> bool:
    return validation_passed and user_action in {"extend_existing", "fork_new_version", "create_new", "create_as_draft"}
