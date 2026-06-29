"""Configuration loading for strategy modules."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_strategy_config(path: str | Path = "config/strategy.yaml") -> dict[str, Any]:
    """Load a simple nested strategy YAML configuration file.

    The project configuration intentionally uses a small YAML subset made of
    nested mappings and scalar values, so the loader has no third-party runtime
    dependency.
    """
    config_path = Path(path)
    config = _parse_nested_mapping(config_path.read_text(encoding="utf-8"))

    if "strategy" not in config:
        raise ValueError("strategy config must contain a top-level 'strategy' key")
    return config


def _parse_nested_mapping(content: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if ":" not in stripped:
            raise ValueError(f"invalid config line {line_number}: expected key/value mapping")

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise ValueError(f"invalid config line {line_number}: empty key")

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"invalid config line {line_number}: bad indentation")

        parent = stack[-1][1]
        if raw_value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _parse_scalar(raw_value)

    return root


def _parse_scalar(value: str) -> str | int | float | bool:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        return value.strip('"\'')
