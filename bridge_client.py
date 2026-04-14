"""Bridge client for schema-driven Figma extraction.

Minimal compatibility layer for existing scripts:
- send(code: str)
- read()
- status()
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "http://localhost:8768"


class BridgeError(RuntimeError):
    """Raised when bridge request fails."""


def _http_json(method: str, path: str, payload: Optional[Dict[str, Any]] = None, timeout: int = 35) -> Dict[str, Any]:
    body = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    request = Request(f"{BASE_URL}{path}", data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
            data = json.loads(text) if text else {}
            if isinstance(data, dict) and "error" in data:
                raise BridgeError(json.dumps(data, ensure_ascii=False))
            return data
    except HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        raise BridgeError(detail or str(e)) from e
    except URLError as e:
        raise BridgeError(str(e)) from e


def send(code: str) -> Any:
    """Execute IIFE JavaScript in Figma plugin and return parsed result."""
    data = _http_json("POST", "/send", {"code": code}, timeout=35)
    result = data.get("result")
    if isinstance(result, str):
        try:
            return json.loads(result)
        except Exception:
            return result
    return result


def read() -> Any:
    """Read current selection from Figma plugin and return structured payload."""
    data = _http_json("POST", "/read", {}, timeout=15)
    result = data.get("result")
    if isinstance(result, str):
        try:
            return json.loads(result)
        except Exception:
            return result
    return result


def status() -> Dict[str, Any]:
    """Fetch bridge status."""
    return _http_json("GET", "/status", None, timeout=5)
