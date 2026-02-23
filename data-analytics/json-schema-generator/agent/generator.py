"""JSON Schema generator — infer JSON Schema from sample data."""
from __future__ import annotations
import json
from dataclasses import dataclass, field

def infer_type(value) -> str:
    if value is None: return "null"
    if isinstance(value, bool): return "boolean"
    if isinstance(value, int): return "integer"
    if isinstance(value, float): return "number"
    if isinstance(value, str): return "string"
    if isinstance(value, list): return "array"
    if isinstance(value, dict): return "object"
    return "string"

def infer_string_format(value: str) -> str | None:
    import re
    if re.match(r"^\d{4}-\d{2}-\d{2}T", value): return "date-time"
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value): return "date"
    if re.match(r"^[^@]+@[^@]+\.[^@]+$", value): return "email"
    if re.match(r"^https?://", value): return "uri"
    if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", value, re.I): return "uuid"
    return None

def generate_schema(data, title: str = "Root", draft: str = "2020-12") -> dict:
    """Generate JSON Schema from sample data."""
    schema = {"$schema": f"https://json-schema.org/draft/{draft}/schema", "title": title}
    schema.update(_infer_schema(data))
    return schema

def _infer_schema(value) -> dict:
    t = infer_type(value)
    if t == "object" and isinstance(value, dict):
        props = {}
        required = []
        for k, v in value.items():
            props[k] = _infer_schema(v)
            required.append(k)
        return {"type": "object", "properties": props, "required": sorted(required)}
    elif t == "array" and isinstance(value, list):
        if not value: return {"type": "array", "items": {}}
        # Merge schemas from multiple items
        item_schemas = [_infer_schema(item) for item in value]
        if all(s == item_schemas[0] for s in item_schemas):
            return {"type": "array", "items": item_schemas[0]}
        # Union type
        types = list(set(s.get("type", "string") for s in item_schemas))
        if len(types) == 1: return {"type": "array", "items": item_schemas[0]}
        return {"type": "array", "items": {"oneOf": item_schemas}}
    elif t == "string" and isinstance(value, str):
        schema = {"type": "string"}
        fmt = infer_string_format(value)
        if fmt: schema["format"] = fmt
        return schema
    elif t == "null":
        return {"type": "null"}
    else:
        return {"type": t}

def generate_from_json(json_str: str, title: str = "Root") -> dict:
    data = json.loads(json_str)
    if isinstance(data, list) and data:
        data = data[0]
    return generate_schema(data, title=title)

def validate_against_schema(data: dict, schema: dict) -> list[str]:
    """Simple validator — check required fields and types."""
    errors = []
    if schema.get("type") == "object":
        for req in schema.get("required", []):
            if req not in data: errors.append(f"Missing required field: {req}")
        for prop, prop_schema in schema.get("properties", {}).items():
            if prop in data:
                expected = prop_schema.get("type")
                actual = infer_type(data[prop])
                if expected and actual != expected and not (expected == "number" and actual == "integer"):
                    errors.append(f"Type mismatch for '{prop}': expected {expected}, got {actual}")
    return errors

def format_schema(schema: dict) -> str:
    return json.dumps(schema, indent=2)
