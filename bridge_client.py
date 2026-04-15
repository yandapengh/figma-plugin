"""Minimal Python client for OpenHarness Figma Bridge."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib import request
from urllib.error import HTTPError, URLError

BASE_URL = "http://localhost:8768"


class BridgeClientError(RuntimeError):
    """Raised when bridge endpoint is unavailable or returns an error."""


def _post(path: str, payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return _send(req, timeout=timeout)


def _get(path: str, timeout: int = 10) -> Dict[str, Any]:
    req = request.Request(f"{BASE_URL}{path}", method="GET")
    return _send(req, timeout=timeout)


def _send(req: request.Request, timeout: int) -> Dict[str, Any]:
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = {"error": {"code": "http_error", "message": body or str(exc)}}
        raise BridgeClientError(payload.get("error", {}).get("message", str(exc))) from exc
    except URLError as exc:
        raise BridgeClientError(f"Bridge unreachable: {exc.reason}") from exc


def send(code: str, *, timeout: int = 30) -> Dict[str, Any]:
    """Send JS code to the bridge /send endpoint."""
    return _post("/send", {"code": code}, timeout=timeout)


def read(*, timeout: int = 10) -> Dict[str, Any]:
    """Read current Figma selection from bridge /read endpoint."""
    return _post("/read", {}, timeout=timeout)


def status(*, timeout: int = 10) -> Dict[str, Any]:
    """Check bridge connection state from /status endpoint."""
    return _get("/status", timeout=timeout)


def ping(*, timeout: int = 10) -> bool:
    """Convenience helper for connection checks."""
    state: Optional[Dict[str, Any]] = status(timeout=timeout)
    return bool(state and state.get("connected"))
