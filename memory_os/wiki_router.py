"""Wiki routing state machine for human-confirmed category placement."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

ROUTE_MODES = {"existing", "new_under_existing", "new_top_level", "no_route"}
INVALID_CATEGORY_CHARS = re.compile(r"[\\/:*?\"<>|]")
PATH_REPEATED_SLASH = re.compile(r"//+")


class WikiRouterError(ValueError):
    """Raised when router input/answer is invalid."""


@dataclass
class RouterQuestion:
    question_id: str
    prompt: str
    candidates: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class RouterStepResult:
    done: bool
    question: Optional[RouterQuestion]
    route: Optional[Dict[str, Any]]


class WikiRouter:
    """Strongly-ordered question workflow for wiki placement routing."""

    def __init__(
        self,
        category_tree_markdown: str,
        content_summary: str,
        recommendations: Optional[List[str]] = None,
    ) -> None:
        self.category_tree_markdown = category_tree_markdown
        self.content_summary = content_summary
        self.recommendations = recommendations or []
        self.candidate_paths = _parse_candidate_paths(category_tree_markdown)
        self.state = "S1"
        self.answers: Dict[str, Any] = {}
        self.audit_log: List[Dict[str, str]] = []

    def next_question(self) -> RouterQuestion:
        if self.state == "S1":
            return RouterQuestion(
                question_id="S1.select_position",
                prompt="请选择放入 wiki 的位置。",
                candidates=self.candidate_paths,
                recommendations=self.recommendations,
            )
        if self.state == "S2":
            return RouterQuestion(
                question_id="S2.create_new_category",
                prompt="当前分类不匹配，是否新建分类？（yes/no）",
            )
        if self.state == "S3a":
            return RouterQuestion(
                question_id="S3a.select_parent",
                prompt="请选择新分类挂载的父路径（parent_path）。",
                candidates=self.candidate_paths,
            )
        if self.state == "S3b":
            return RouterQuestion(
                question_id="S3b.new_top_level",
                prompt="请输入顶层分类名（new_category_name），可选描述（new_category_description）。",
            )
        if self.state == "S4":
            return RouterQuestion(
                question_id="S4.confirm",
                prompt="请确认最终路由信息（confirm=true/false）。",
            )
        raise WikiRouterError(f"Unknown router state: {self.state}")

    def submit_answer(self, question_id: str, answer: Dict[str, Any]) -> RouterStepResult:
        expected = self.next_question().question_id
        if question_id != expected:
            raise WikiRouterError(f"question_id mismatch: expected {expected}, got {question_id}")

        self._log_round(question_id, answer)

        if self.state == "S1":
            self._handle_s1(answer)
        elif self.state == "S2":
            self._handle_s2(answer)
        elif self.state == "S3a":
            self._handle_s3a(answer)
        elif self.state == "S3b":
            self._handle_s3b(answer)
        elif self.state == "S4":
            self._handle_s4(answer)
        else:
            raise WikiRouterError(f"Unknown router state: {self.state}")

        if self.state == "DONE":
            decision = self.build_route_decision()
            return RouterStepResult(done=True, question=None, route=decision)

        return RouterStepResult(done=False, question=self.next_question(), route=None)

    def build_route_decision(self) -> Dict[str, Any]:
        route_mode = self.answers.get("route_mode")
        decision = {
            "route_mode": route_mode,
            "selected_path": self.answers.get("selected_path"),
            "parent_path": self.answers.get("parent_path"),
            "new_category_name": self.answers.get("new_category_name"),
            "new_category_description": self.answers.get("new_category_description"),
            "user_confirmed": bool(self.answers.get("user_confirmed", False)),
            "rationale": self.answers.get("rationale"),
        }
        validate_route_decision(decision, existing_paths=self.candidate_paths)
        return decision

    def _handle_s1(self, answer: Dict[str, Any]) -> None:
        selected = answer.get("selected_path")
        rationale = answer.get("rationale")
        if selected == "not_matched":
            self.answers["rationale"] = rationale
            self.state = "S2"
            return

        normalized = normalize_path(selected)
        if normalized not in self.candidate_paths:
            raise WikiRouterError("selected_path is not in candidate paths")

        self.answers["route_mode"] = "existing"
        self.answers["selected_path"] = normalized
        self.answers["rationale"] = rationale
        self.state = "S4"

    def _handle_s2(self, answer: Dict[str, Any]) -> None:
        create_new = answer.get("create_new")
        if create_new not in {True, False}:
            raise WikiRouterError("create_new must be true/false")

        if not create_new:
            self.answers["route_mode"] = "no_route"
            self.answers["selected_path"] = None
            self.answers.setdefault("rationale", "no_category_confirmed")
            self.state = "S4"
            return

        under_existing = answer.get("under_existing")
        if under_existing not in {True, False}:
            raise WikiRouterError("under_existing must be true/false when create_new=true")

        self.answers["route_mode"] = "new_under_existing" if under_existing else "new_top_level"
        self.state = "S3a" if under_existing else "S3b"

    def _handle_s3a(self, answer: Dict[str, Any]) -> None:
        parent = normalize_path(answer.get("parent_path"))
        name = answer.get("new_category_name")
        desc = answer.get("new_category_description")

        if parent not in self.candidate_paths:
            raise WikiRouterError("parent_path is not in candidate paths")

        _validate_category_name(name, existing_paths=self.candidate_paths, parent_path=parent)

        self.answers["parent_path"] = parent
        self.answers["new_category_name"] = name.strip()
        self.answers["new_category_description"] = desc
        self.state = "S4"

    def _handle_s3b(self, answer: Dict[str, Any]) -> None:
        name = answer.get("new_category_name")
        desc = answer.get("new_category_description")
        _validate_category_name(name, existing_paths=self.candidate_paths)

        self.answers["new_category_name"] = name.strip()
        self.answers["new_category_description"] = desc
        self.state = "S4"

    def _handle_s4(self, answer: Dict[str, Any]) -> None:
        confirmed = answer.get("user_confirmed")
        if confirmed not in {True, False}:
            raise WikiRouterError("user_confirmed must be true/false")

        self.answers["user_confirmed"] = confirmed
        self.answers["rationale"] = answer.get("rationale", self.answers.get("rationale"))
        self.state = "DONE"

    def _log_round(self, question_id: str, answer: Dict[str, Any]) -> None:
        self.audit_log.append(
            {
                "question_id": question_id,
                "answer": str(answer),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )


def _parse_candidate_paths(markdown: str) -> List[str]:
    """Parse figma-wiki/_index.md headings and bullet links into paths."""

    candidates: List[str] = []
    current_section: Optional[str] = None

    for raw in markdown.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current_section = _slugify(line[3:].split("（")[0].split("(")[0])
            if current_section:
                candidates.append(current_section)
            continue

        if line.startswith("- [") and "](" in line and current_section:
            link_target = line.split("](", 1)[1].split(")", 1)[0]
            parts = [segment for segment in link_target.split("/") if segment and not segment.endswith(".md") and not segment.endswith(".jsx")]
            if not parts:
                continue
            top = _slugify(parts[0])
            if not top:
                continue
            if len(parts) == 1:
                path = top
            else:
                tail = _slugify(parts[1])
                path = f"{top}/{tail}" if tail else top
            candidates.append(path)

    deduped: List[str] = []
    seen = set()
    for item in candidates:
        normalized = normalize_path(item)
        if normalized not in seen:
            seen.add(normalized)
            deduped.append(normalized)

    return deduped


def _slugify(text: str) -> str:
    lowered = text.strip().lower()
    cleaned = re.sub(r"[^a-z0-9_-]+", "-", lowered)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned


def normalize_path(path: Optional[str]) -> str:
    if not isinstance(path, str):
        raise WikiRouterError("path must be a string")

    candidate = path.strip().strip("/")
    if not candidate or PATH_REPEATED_SLASH.search(candidate):
        raise WikiRouterError("path must be in a/b/c format without empty segment")

    segments = [segment.strip() for segment in candidate.split("/")]
    if any(not segment for segment in segments):
        raise WikiRouterError("path must not contain empty segment")

    return "/".join(segments)


def _validate_category_name(name: Any, existing_paths: List[str], parent_path: Optional[str] = None) -> None:
    if not isinstance(name, str):
        raise WikiRouterError("new_category_name must be string")

    normalized = name.strip()
    if len(normalized) < 2 or len(normalized) > 64:
        raise WikiRouterError("new_category_name length must be between 2 and 64")

    if INVALID_CATEGORY_CHARS.search(normalized):
        raise WikiRouterError("new_category_name contains invalid chars")

    target = f"{parent_path}/{normalized}" if parent_path else normalized
    normalized_target = normalize_path(target)
    if normalized_target in existing_paths:
        raise WikiRouterError("new_category_name duplicates existing path")


def validate_route_decision(decision: Dict[str, Any], existing_paths: Optional[List[str]] = None) -> None:
    mode = decision.get("route_mode")
    if mode not in ROUTE_MODES:
        raise WikiRouterError("route_mode invalid")

    if mode == "existing":
        if not decision.get("selected_path"):
            raise WikiRouterError("selected_path is required when route_mode=existing")
        normalize_path(decision["selected_path"])

    if mode == "no_route":
        selected = decision.get("selected_path")
        if selected:
            normalize_path(selected)
        if decision.get("user_confirmed") not in {True, False}:
            raise WikiRouterError("user_confirmed must be true/false when route_mode=no_route")

    if mode == "new_under_existing":
        if not decision.get("parent_path"):
            raise WikiRouterError("parent_path is required when route_mode=new_under_existing")
        normalize_path(decision["parent_path"])
        _validate_category_name(
            decision.get("new_category_name"),
            existing_paths=existing_paths or [],
            parent_path=decision.get("parent_path"),
        )

    if mode == "new_top_level":
        _validate_category_name(decision.get("new_category_name"), existing_paths=existing_paths or [])
