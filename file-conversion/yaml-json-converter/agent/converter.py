"""YAML-JSON converter — bidirectional conversion between YAML and JSON."""
from __future__ import annotations
import json, re

def json_to_yaml(data, indent: int = 0) -> str:
    """Convert JSON data to YAML string."""
    lines = []
    pad = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)) and value:
                lines.append(f"{pad}{key}:")
                lines.append(json_to_yaml(value, indent + 1))
            elif isinstance(value, bool):
                lines.append(f"{pad}{key}: {'true' if value else 'false'}")
            elif value is None:
                lines.append(f"{pad}{key}: null")
            elif isinstance(value, str):
                if "\n" in value:
                    lines.append(f"{pad}{key}: |")
                    for vl in value.split("\n"): lines.append(f"{pad}  {vl}")
                elif any(c in value for c in ":#{}[]&*!|>'\""):
                    lines.append(f'{pad}{key}: "{value}"')
                else:
                    lines.append(f"{pad}{key}: {value}")
            else:
                lines.append(f"{pad}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(json_to_yaml(item, indent + 1))
            elif isinstance(item, bool):
                lines.append(f"{pad}- {'true' if item else 'false'}")
            elif item is None:
                lines.append(f"{pad}- null")
            elif isinstance(item, str):
                lines.append(f"{pad}- {item}")
            else:
                lines.append(f"{pad}- {item}")
    return "\n".join(lines)

def yaml_to_json(yaml_str: str) -> dict | list:
    """Parse simple YAML to Python dict/list (no external deps)."""
    lines = yaml_str.strip().split("\n")
    return _parse_yaml_lines(lines, 0)[0]

def _get_indent(line: str) -> int:
    return len(line) - len(line.lstrip())

def _parse_value(value: str):
    v = value.strip()
    if v in ("true", "True", "yes"): return True
    if v in ("false", "False", "no"): return False
    if v in ("null", "~", ""): return None
    if v.startswith('"') and v.endswith('"'): return v[1:-1]
    if v.startswith("'") and v.endswith("'"): return v[1:-1]
    try: return int(v)
    except ValueError: pass
    try: return float(v)
    except ValueError: pass
    return v

def _parse_yaml_lines(lines: list[str], base_indent: int) -> tuple:
    if not lines: return {}, 0
    first = lines[0]
    stripped = first.lstrip()
    if stripped.startswith("- "):
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            ind = _get_indent(line)
            if ind < base_indent and i > 0: break
            s = line.lstrip()
            if s.startswith("- "):
                val = s[2:].strip()
                if ":" in val and not val.startswith('"'):
                    # inline dict
                    k, _, v = val.partition(":")
                    result.append({k.strip(): _parse_value(v)})
                else:
                    result.append(_parse_value(val))
                i += 1
            else:
                i += 1
        return result, i
    else:
        result = {}
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.strip() or line.lstrip().startswith("#"):
                i += 1; continue
            ind = _get_indent(line)
            if ind < base_indent and i > 0: break
            s = line.lstrip()
            if ":" in s:
                key, _, val = s.partition(":")
                key = key.strip()
                val = val.strip()
                if val:
                    result[key] = _parse_value(val)
                    i += 1
                else:
                    # nested
                    child_lines = []
                    j = i + 1
                    while j < len(lines):
                        if lines[j].strip() and _get_indent(lines[j]) <= ind: break
                        child_lines.append(lines[j])
                        j += 1
                    if child_lines:
                        child_indent = _get_indent(child_lines[0])
                        result[key], _ = _parse_yaml_lines(child_lines, child_indent)
                    else:
                        result[key] = None
                    i = j
            else:
                i += 1
        return result, i

def convert_json_string_to_yaml(json_str: str) -> str:
    data = json.loads(json_str)
    return json_to_yaml(data)

def convert_yaml_string_to_json(yaml_str: str, indent: int = 2) -> str:
    data = yaml_to_json(yaml_str)
    return json.dumps(data, indent=indent)

def detect_format(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("{") or stripped.startswith("["): return "json"
    return "yaml"
