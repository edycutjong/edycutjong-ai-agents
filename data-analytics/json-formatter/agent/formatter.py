"""JSON formatter — format, validate, minify, and analyze JSON data."""
from __future__ import annotations
import json
from dataclasses import dataclass, field

@dataclass
class JSONResult:
    is_valid: bool = True; error: str = ""; key_count: int = 0; depth: int = 0
    size_bytes: int = 0; formatted: str = ""; minified: str = ""
    def to_dict(self) -> dict: return {"is_valid": self.is_valid, "key_count": self.key_count, "depth": self.depth}

def _count_keys(obj, depth=0) -> tuple[int, int]:
    if isinstance(obj, dict):
        total_keys = len(obj); max_depth = depth + 1
        for v in obj.values():
            k, d = _count_keys(v, depth + 1)
            total_keys += k; max_depth = max(max_depth, d)
        return total_keys, max_depth
    elif isinstance(obj, list):
        total_keys = 0; max_depth = depth
        for v in obj:
            k, d = _count_keys(v, depth)
            total_keys += k; max_depth = max(max_depth, d)
        return total_keys, max_depth
    return 0, depth

def format_json(text: str, indent: int = 2, sort_keys: bool = False) -> JSONResult:
    r = JSONResult(size_bytes=len(text.encode()))
    try:
        data = json.loads(text)
        r.formatted = json.dumps(data, indent=indent, sort_keys=sort_keys)
        r.minified = json.dumps(data, separators=(",", ":"))
        keys, depth = _count_keys(data)
        r.key_count = keys; r.depth = depth
    except json.JSONDecodeError as e:
        r.is_valid = False; r.error = str(e)
    return r

def extract_paths(text: str) -> list[str]:
    def _walk(obj, path="$"):
        paths = [path]
        if isinstance(obj, dict):
            for k, v in obj.items(): paths.extend(_walk(v, f"{path}.{k}"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj): paths.extend(_walk(v, f"{path}[{i}]"))
        return paths
    try: return _walk(json.loads(text))
    except: return []

def get_value(text: str, key: str) -> str:
    try:
        data = json.loads(text)
        return str(data.get(key, "")) if isinstance(data, dict) else ""
    except: return ""

def sort_keys_recursive(text: str) -> str:
    try: return json.dumps(json.loads(text), indent=2, sort_keys=True)
    except: return text

def format_result_markdown(r: JSONResult) -> str:
    if not r.is_valid: return f"## JSON Formatter ❌\n**Error:** {r.error}"
    compact = r.minified[:100] + ("..." if len(r.minified) > 100 else "")
    return f"## JSON Formatter ✅\n**Keys:** {r.key_count} | **Depth:** {r.depth} | **Size:** {r.size_bytes}B\n```json\n{compact}\n```"
