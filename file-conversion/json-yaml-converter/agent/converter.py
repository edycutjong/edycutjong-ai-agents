"""JSON ↔ YAML ↔ TOML conversion engine."""
from __future__ import annotations

import json
import re


def _yaml_dump(data, indent=2, _level=0):
    """Simple YAML serializer (no PyYAML dependency)."""
    lines = []
    prefix = " " * indent * _level

    if isinstance(data, dict):
        if not data:
            return "{}"
        for key, value in data.items():
            key_str = str(key)
            if isinstance(value, (dict, list)):
                if not value:
                    lines.append(f"{prefix}{key_str}: {'{}' if isinstance(value, dict) else '[]'}")
                else:
                    lines.append(f"{prefix}{key_str}:")
                    lines.append(_yaml_dump(value, indent, _level + 1))
            else:
                lines.append(f"{prefix}{key_str}: {_yaml_value(value)}")
    elif isinstance(data, list):
        if not data:
            return "[]"
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(_yaml_dump(item, indent, _level + 1))
            else:
                lines.append(f"{prefix}- {_yaml_value(item)}")
    else:
        return f"{prefix}{_yaml_value(data)}"

    return "\n".join(lines)


def _yaml_value(value):
    """Format a scalar value for YAML."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    # Quote strings that could be misinterpreted
    if s in ("true", "false", "null", "") or s.startswith("{") or s.startswith("["):
        return f'"{s}"'
    if ":" in s or "#" in s or s.startswith("-") or s.startswith("'"):
        return f'"{s}"'
    return s


def _yaml_parse(text: str) -> dict | list | str:
    """Simple YAML parser for common cases. Falls back to treating as string."""
    lines = text.strip().split("\n")
    if not lines:
        return {}

    # Try JSON first (valid YAML is often valid JSON)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    result = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value == "" or value == "null":
                result[key] = None
            elif value in ("true", "True"):
                result[key] = True
            elif value in ("false", "False"):
                result[key] = False
            elif value.startswith('"') and value.endswith('"'):
                result[key] = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                result[key] = value[1:-1]
            else:
                try:
                    result[key] = int(value)
                except ValueError:
                    try:
                        result[key] = float(value)
                    except ValueError:
                        result[key] = value
    return result


def _toml_dump(data, _prefix=""):
    """Simple TOML serializer for flat/nested dicts."""
    lines = []
    tables = []

    for key, value in data.items():
        if isinstance(value, dict):
            table_key = f"{_prefix}{key}" if _prefix else key
            tables.append((table_key, value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, (str, int, float, bool)):
                    lines.append(f"{key} = {_toml_value(value)}")
                    break
        else:
            lines.append(f"{key} = {_toml_value(value)}")

    for table_key, table_data in tables:
        lines.append(f"\n[{table_key}]")
        lines.append(_toml_dump(table_data, f"{table_key}."))

    return "\n".join(lines)


def _toml_value(value):
    """Format a scalar for TOML."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, list):
        items = ", ".join(_toml_value(v) for v in value)
        return f"[{items}]"
    return f'"{value}"'


# --- Public API ---

def json_to_yaml(json_str: str, indent: int = 2) -> str:
    """Convert JSON string to YAML."""
    data = json.loads(json_str)
    return _yaml_dump(data, indent=indent)


def yaml_to_json(yaml_str: str, indent: int = 2) -> str:
    """Convert YAML string to JSON."""
    data = _yaml_parse(yaml_str)
    return json.dumps(data, indent=indent)


def json_to_toml(json_str: str) -> str:
    """Convert JSON string to TOML."""
    data = json.loads(json_str)
    if not isinstance(data, dict):
        raise ValueError("TOML requires a top-level table (dict)")
    return _toml_dump(data)


def validate_json(text: str) -> dict:
    """Validate JSON and return info."""
    try:
        data = json.loads(text)
        return {
            "valid": True,
            "type": type(data).__name__,
            "keys": list(data.keys()) if isinstance(data, dict) else None,
            "length": len(data) if isinstance(data, (dict, list)) else None,
        }
    except json.JSONDecodeError as e:
        return {"valid": False, "error": str(e), "line": e.lineno, "col": e.colno}


def format_json(text: str, indent: int = 2, sort_keys: bool = False, compact: bool = False) -> str:
    """Pretty-print or minify JSON."""
    data = json.loads(text)
    if compact:
        return json.dumps(data, separators=(",", ":"), sort_keys=sort_keys)
    return json.dumps(data, indent=indent, sort_keys=sort_keys)


def detect_format(text: str) -> str:
    """Detect if text is JSON, YAML, TOML, or unknown."""
    stripped = text.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            json.loads(stripped)
            return "json"
        except json.JSONDecodeError:
            pass
    if "---" in stripped[:10] or (re.search(r"^\w+:", stripped, re.MULTILINE) and not stripped.startswith("{")):
        return "yaml"
    if re.search(r"^\[.+\]$", stripped, re.MULTILINE) and "=" in stripped:
        return "toml"
    return "unknown"


def convert(text: str, target_format: str, source_format: str | None = None) -> str:
    """Auto-detect source and convert to target format."""
    if not source_format:
        source_format = detect_format(text)

    if source_format == target_format:
        return text

    # Parse to intermediate dict
    if source_format == "json":
        data = json.loads(text)
    elif source_format == "yaml":
        data = _yaml_parse(text)
    else:
        raise ValueError(f"Cannot parse source format: {source_format}")

    # Serialize to target
    if target_format == "json":
        return json.dumps(data, indent=2)
    elif target_format == "yaml":
        return _yaml_dump(data)
    elif target_format == "toml":
        if not isinstance(data, dict):
            raise ValueError("TOML requires dict input")
        return _toml_dump(data)
    else:
        raise ValueError(f"Unknown target format: {target_format}")
