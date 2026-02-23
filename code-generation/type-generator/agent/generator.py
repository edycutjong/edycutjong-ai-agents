"""Type generator — infer TypeScript/Python types from JSON data."""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field

@dataclass
class TypeField:
    name: str
    type_str: str
    optional: bool = False
    children: list["TypeField"] = field(default_factory=list)

def infer_json_type(value) -> str:
    if value is None: return "null"
    if isinstance(value, bool): return "boolean"
    if isinstance(value, int): return "number"
    if isinstance(value, float): return "number"
    if isinstance(value, str): return "string"
    if isinstance(value, list): return "array"
    if isinstance(value, dict): return "object"
    return "any"

def infer_fields(data: dict, prefix: str = "") -> list[TypeField]:
    fields = []
    for key, value in data.items():
        t = infer_json_type(value)
        children = []
        if t == "object" and isinstance(value, dict):
            children = infer_fields(value, prefix=f"{prefix}{key}.")
        elif t == "array" and isinstance(value, list) and value:
            if isinstance(value[0], dict):
                children = infer_fields(value[0], prefix=f"{prefix}{key}[].")
                t = "object[]"
            else:
                t = f"{infer_json_type(value[0])}[]"
        fields.append(TypeField(name=key, type_str=t, children=children))
    return fields

def to_typescript(fields: list[TypeField], name: str = "Root", indent: int = 0) -> str:
    pad = "  " * indent
    lines = [f"{pad}interface {name} {{"]
    ts_map = {"string": "string", "number": "number", "boolean": "boolean", "null": "null", "any": "any"}
    for f in fields:
        opt = "?" if f.optional else ""
        if f.type_str == "object" and f.children:
            lines.append(f"{pad}  {f.name}{opt}: {{")
            for c in f.children:
                ct = ts_map.get(c.type_str, c.type_str)
                lines.append(f"{pad}    {c.name}: {ct};")
            lines.append(f"{pad}  }};")
        elif f.type_str == "object[]" and f.children:
            lines.append(f"{pad}  {f.name}{opt}: {{")
            for c in f.children:
                ct = ts_map.get(c.type_str, c.type_str)
                lines.append(f"{pad}    {c.name}: {ct};")
            lines.append(f"{pad}  }}[];")
        else:
            ts_type = ts_map.get(f.type_str, f.type_str)
            lines.append(f"{pad}  {f.name}{opt}: {ts_type};")
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def to_python_dataclass(fields: list[TypeField], name: str = "Root") -> str:
    py_map = {"string": "str", "number": "float", "boolean": "bool", "null": "None", "any": "Any", "number[]": "list[float]", "string[]": "list[str]", "boolean[]": "list[bool]"}
    lines = ["from dataclasses import dataclass, field", "from typing import Any, Optional", "", f"@dataclass", f"class {name}:"]
    for f in fields:
        py_type = py_map.get(f.type_str, f.type_str)
        if f.type_str == "object" and f.children:
            py_type = "dict"
        elif f.type_str == "object[]":
            py_type = "list[dict]"
        opt = f"Optional[{py_type}]" if f.optional else py_type
        default = " = None" if f.optional else ""
        lines.append(f"    {f.name}: {opt}{default}")
    return "\n".join(lines)

def to_zod_schema(fields: list[TypeField], name: str = "Root") -> str:
    zod_map = {"string": "z.string()", "number": "z.number()", "boolean": "z.boolean()", "null": "z.null()", "any": "z.any()"}
    lines = ['import { z } from "zod";', "", f"const {name}Schema = z.object({{"]
    for f in fields:
        zt = zod_map.get(f.type_str 	, "z.any()")
        if f.type_str.endswith("[]"):
            base = f.type_str[:-2]
            zt = f"z.array({zod_map.get(base, 'z.any()')})"
        if f.type_str in ("object", "object[]"):
            zt = "z.record(z.any())" if f.type_str == "object" else "z.array(z.record(z.any()))"
        if f.optional: zt += ".optional()"
        lines.append(f"  {f.name}: {zt},")
    lines.append("});")
    lines.append(f"\ntype {name} = z.infer<typeof {name}Schema>;")
    return "\n".join(lines)

def generate_types(json_data: str | dict, name: str = "Root", fmt: str = "typescript") -> str:
    if isinstance(json_data, str): json_data = json.loads(json_data)
    if isinstance(json_data, list):
        json_data = json_data[0] if json_data else {}
    fields = infer_fields(json_data)
    if fmt == "typescript": return to_typescript(fields, name)
    if fmt == "python": return to_python_dataclass(fields, name)
    if fmt == "zod": return to_zod_schema(fields, name)
    return to_typescript(fields, name)
