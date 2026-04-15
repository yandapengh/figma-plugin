"""Human-in-the-loop decision gate: never persist without explicit approval."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from memory_os.wiki_router import validate_route_decision


DEFAULT_WIKI_TARGETS = ["tokens", "components", "pages", "tooling"]


def _derive_wiki_target_candidates(delta: Dict[str, Any], validation_report: Dict[str, Any]) -> List[str]:
    """Infer wiki target candidates from wiki index hints and payload content."""

    candidates: List[str] = []

    wiki_index = validation_report.get("wiki_index")
    if isinstance(wiki_index, dict):
        candidates.extend(str(key) for key in wiki_index.keys())
    elif isinstance(wiki_index, list):
        candidates.extend(str(item) for item in wiki_index)

    key_space = " ".join(str(key).lower() for key in delta.keys())
    hints = {
        "tokens": ("token", "color", "typography", "effect"),
        "components": ("component", "variant", "semantics"),
        "pages": ("page", "screen", "flow"),
        "tooling": ("tool", "plugin", "automation", "workflow", "script"),
    }
    for target, keywords in hints.items():
        if any(keyword in key_space for keyword in keywords):
            candidates.append(target)

    if not candidates:
        candidates.extend(DEFAULT_WIKI_TARGETS)

    deduped: List[str] = []
    seen = set()
    for candidate in candidates:
        normalized = candidate.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(normalized)

    return deduped


def _estimate_wiki_target_confidence(candidates: List[str], delta: Dict[str, Any]) -> Optional[float]:
    """Return a simple confidence score for the top inferred target."""

    if not candidates:
        return None

    if candidates[0] in delta:
        return 0.9
    if len(candidates) == 1:
        return 0.75
    return 0.6


def build_decision_payload(case_type: str, delta: Dict[str, Any], validation_report: Dict[str, Any]) -> Dict[str, Any]:
    if case_type not in {"similar_page", "new_page"}:
        raise ValueError("case_type must be similar_page or new_page")

    wiki_target_candidates = _derive_wiki_target_candidates(delta, validation_report)

    return {
        "case": case_type,
        "validation": validation_report,
        "delta": delta,
        "allowed_actions": (
            ["extend_existing", "fork_new_version", "reject"]
            if case_type == "similar_page"
            else ["create_new", "create_as_draft", "reject"]
        ),
        "wiki_target_candidates": wiki_target_candidates,
        "wiki_target_selected": None,
        "wiki_target_confidence": _estimate_wiki_target_confidence(wiki_target_candidates, delta),
        "requires_wiki_target_confirmation": True,
        "write_allowed": False,
        "requires_user_confirmation": True,
    }


def can_persist(
    user_action: str,
    validation_passed: bool,
    wiki_target_selected: Optional[str] = None,
    requires_wiki_target_confirmation: bool = True,
) -> bool:
    action_confirmed = user_action in {"extend_existing", "fork_new_version", "create_new", "create_as_draft"}
    if not (validation_passed and action_confirmed):
        return False

    if requires_wiki_target_confirmation and not wiki_target_selected:
        return False

    return True


def prepare_wiki_write(decision_payload: Dict[str, Any], wiki_route: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Attach wiki routing decision before write stage with minimal compatibility impact."""

    result = dict(decision_payload)
    result.setdefault("wiki_target_selected", None)

    if not isinstance(wiki_route, dict):
        result["write_allowed"] = False
        result["write_status"] = "pending_confirmation"
        result["route_decision"] = None
        return result

    validate_route_decision(wiki_route)

    user_confirmed = bool(wiki_route.get("user_confirmed"))
    result["route_decision"] = wiki_route
    result["write_allowed"] = user_confirmed
    result["write_status"] = "ready" if user_confirmed else "pending_confirmation"

    if wiki_route.get("route_mode") == "existing":
        result["wiki_target_selected"] = wiki_route.get("selected_path")

    return result
