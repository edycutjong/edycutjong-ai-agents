"""YAML validator — parse, validate, and convert YAML data."""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field

@dataclass
class YAMLResult:
    is_valid: bool = True; error: str = ""; line_count: int = 0
    key_count: int = 0; data: dict = None; as_json: str = ""
    def to_dict(self) -> dict: return {"is_valid": self.is_valid, "keys": self.key_count, "lines": self.line_count}

def _simple_parse(text: str) -> dict:
    result = {}; current = result; stack = [(result, -1)]
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"): continue
        indent = len(line) - len(line.lstrip())
        m = re.match(r'^([^:]+):\s*(.*)', stripped)
        if m:
            key, val = m.group(1).strip(), m.group(2).strip()
            while stack and stack[-1][1] >= indent: stack.pop()
            current = stack[-1][0] if stack else result
            if val:
                if val.lower() == "true": val = True
                elif val.lower() == "false": val = False
                elif val.replace(".", "").replace("-", "").isdigit():
                    try: val = int(val) if "." not in val else float(val)
                    except: pass
                elif val.startswith('"') and val.endswith('"'): val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"): val = val[1:-1]
                current[key] = val
            else:
                current[key] = {}; stack.append((current[key], indent))
    return result

def _count_keys(d) -> int:
    if not isinstance(d, dict): return 0
    return len(d) + sum(_count_keys(v) for v in d.values())

def validate_yaml(text: str) -> YAMLResult:
    r = YAMLResult(line_count=text.count("\n") + 1)
    try:
        r.data = _simple_parse(text); r.key_count = _count_keys(r.data)
        r.as_json = json.dumps(r.data, indent=2)
    except Exception as e:
        r.is_valid = False; r.error = str(e)
    return r

def yaml_to_json(text: str) -> str:
    d = _simple_parse(text); return json.dumps(d, indent=2)

def get_keys(text: str) -> list[str]:
    d = _simple_parse(text)
    def _walk(obj, prefix=""):
        keys = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.append(f"{prefix}{k}" if not prefix else f"{prefix}.{k}")
                keys.extend(_walk(v, f"{prefix}{k}."))
        return keys
    return _walk(d)

def format_result_markdown(r: YAMLResult) -> str:
    if not r.is_valid: return f"## YAML Validator ❌\n**Error:** {r.error}"
    return f"## YAML Validator ✅\n**Lines:** {r.line_count} | **Keys:** {r.key_count}"
