"""Safely render local billing API JSON as Markdown."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = ("method", "path", "summary", "auth", "owner")
_NOT_FOUND = "Not Found"
_SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_ -]?key|access[_ -]?token|client[_ -]?secret|password|secret|credential)\b"),
    re.compile(r"(?i)\bBearer\s+\S+"),
    re.compile(r"\b(?:sk|pk)_(?:live|test)_[A-Za-z0-9]{8,}\b"),
)


class SyncError(ValueError):
    """Raised when input is invalid or paths are unsafe."""


def _within_root(path: str | os.PathLike[str], root: Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise SyncError(f"Path escapes repository root: {path}") from exc
    return resolved


def _is_empty(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _contains_secret(value: Any) -> bool:
    text = value if isinstance(value, str) else str(value)
    return any(pattern.search(text) for pattern in _SECRET_PATTERNS)


def _display(value: Any) -> str:
    if _is_empty(value) or _contains_secret(value):
        return _NOT_FOUND
    text = str(value).strip()
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _render(endpoints: list[dict[str, Any]]) -> str:
    lines = ["# Billing API", "", "Generated from `sources/billing-api.json`.", ""]
    if not endpoints:
        lines.extend(["No endpoints are defined.", ""])
        return "\n".join(lines)
    for index, endpoint in enumerate(endpoints):
        if index:
            lines.append("")
        lines.extend([f"## {_display(endpoint.get('method'))} {_display(endpoint.get('path'))}", ""])
        for field in REQUIRED_FIELDS:
            lines.append(f"- **{field.title()}:** {_display(endpoint.get(field))}")
    lines.append("")
    return "\n".join(lines)


def sync(
    source_path: str | os.PathLike[str] = "sources/billing-api.json",
    output_path: str | os.PathLike[str] = "docs/API.md",
    *,
    root: str | os.PathLike[str] | None = None,
) -> Path:
    """Validate and synchronize local JSON; invalid sources never alter output."""
    repository = Path(root or Path.cwd()).resolve()
    source = _within_root(source_path, repository)
    output = _within_root(output_path, repository)
    try:
        raw = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise SyncError(f"Cannot read source file: {source}") from exc
    if not raw.strip():
        raise SyncError("Source file is empty")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SyncError("Source is not valid JSON") from exc
    if not isinstance(data, dict) or not isinstance(data.get("endpoints"), list):
        raise SyncError("Source must be an object containing an endpoints array")
    if any(not isinstance(endpoint, dict) for endpoint in data["endpoints"]):
        raise SyncError("Every endpoint must be an object")

    content = _render(data["endpoints"])
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=output.parent, delete=False
        ) as temporary:
            temp_name = temporary.name
            temporary.write(content)
        os.replace(temp_name, output)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
    return output
