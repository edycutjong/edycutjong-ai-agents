"""GraphQL schema analyzer — parse, validate, and analyze GraphQL SDL schemas."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class FieldInfo:
    name: str
    field_type: str
    is_required: bool = False
    is_list: bool = False
    args: list[str] = field(default_factory=list)
    description: str = ""

@dataclass
class TypeInfo:
    name: str
    kind: str  # type, input, enum, interface, union, scalar
    fields: list[FieldInfo] = field(default_factory=list)
    implements: list[str] = field(default_factory=list)
    values: list[str] = field(default_factory=list)  # enum values
    description: str = ""

    def to_dict(self) -> dict:
        d = {"name": self.name, "kind": self.kind}
        if self.fields:
            d["fields"] = [{"name": f.name, "type": f.field_type, "required": f.is_required, "list": f.is_list} for f in self.fields]
        if self.values:
            d["values"] = self.values
        if self.implements:
            d["implements"] = self.implements
        return d

@dataclass
class SchemaStats:
    types: int = 0
    inputs: int = 0
    enums: int = 0
    interfaces: int = 0
    unions: int = 0
    scalars: int = 0
    queries: int = 0
    mutations: int = 0
    subscriptions: int = 0
    total_fields: int = 0

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v > 0}


def parse_schema(sdl: str) -> list[TypeInfo]:
    """Parse GraphQL SDL into type definitions."""
    types = []

    # Parse type/input/interface definitions
    type_pattern = r'(?:"""[^"]*"""\s*)?(?:type|input|interface)\s+(\w+)(?:\s+implements\s+([\w\s&]+))?\s*\{([^}]*)\}'
    for match in re.finditer(type_pattern, sdl):
        name = match.group(1)
        implements = [i.strip() for i in match.group(2).split("&")] if match.group(2) else []
        body = match.group(3)

        kind = "type"
        if f"input {name}" in sdl:
            kind = "input"
        elif f"interface {name}" in sdl:
            kind = "interface"

        fields = _parse_fields(body)
        types.append(TypeInfo(name=name, kind=kind, fields=fields, implements=implements))

    # Parse enums
    enum_pattern = r'enum\s+(\w+)\s*\{([^}]*)\}'
    for match in re.finditer(enum_pattern, sdl):
        values = [v.strip() for v in match.group(2).strip().split("\n") if v.strip() and not v.strip().startswith("#")]
        types.append(TypeInfo(name=match.group(1), kind="enum", values=values))

    # Parse unions
    union_pattern = r'union\s+(\w+)\s*=\s*(.+?)(?:\n|$)'
    for match in re.finditer(union_pattern, sdl):
        members = [m.strip() for m in match.group(2).split("|")]
        types.append(TypeInfo(name=match.group(1), kind="union", values=members))

    # Parse scalars
    scalar_pattern = r'scalar\s+(\w+)'
    for match in re.finditer(scalar_pattern, sdl):
        types.append(TypeInfo(name=match.group(1), kind="scalar"))

    return types


def _parse_fields(body: str) -> list[FieldInfo]:
    """Parse fields from a type body."""
    fields = []
    field_pattern = r'(\w+)(?:\(([^)]*)\))?\s*:\s*(\[?\w+!?\]?!?)'
    for match in re.finditer(field_pattern, body):
        name = match.group(1)
        args_str = match.group(2) or ""
        type_str = match.group(3)

        is_list = type_str.startswith("[")
        is_required = type_str.endswith("!")
        clean_type = type_str.replace("[", "").replace("]", "").replace("!", "")

        args = [a.strip().split(":")[0].strip() for a in args_str.split(",") if a.strip()] if args_str else []

        fields.append(FieldInfo(name=name, field_type=clean_type, is_required=is_required, is_list=is_list, args=args))
    return fields


def get_schema_stats(types: list[TypeInfo]) -> SchemaStats:
    """Calculate schema statistics."""
    stats = SchemaStats()
    for t in types:
        if t.kind == "type":
            stats.types += 1
            if t.name == "Query":
                stats.queries = len(t.fields)
            elif t.name == "Mutation":
                stats.mutations = len(t.fields)
            elif t.name == "Subscription":
                stats.subscriptions = len(t.fields)
        elif t.kind == "input":
            stats.inputs += 1
        elif t.kind == "enum":
            stats.enums += 1
        elif t.kind == "interface":
            stats.interfaces += 1
        elif t.kind == "union":
            stats.unions += 1
        elif t.kind == "scalar":
            stats.scalars += 1
        stats.total_fields += len(t.fields)
    return stats


def find_unused_types(types: list[TypeInfo]) -> list[str]:
    """Find types that aren't referenced by any field."""
    all_names = {t.name for t in types}
    referenced = set()
    for t in types:
        for f in t.fields:
            referenced.add(f.field_type)
        referenced.update(t.implements)
        if t.kind == "union":
            referenced.update(t.values)

    builtins = {"String", "Int", "Float", "Boolean", "ID", "Query", "Mutation", "Subscription"}
    return sorted(all_names - referenced - builtins)


def find_complexity_issues(types: list[TypeInfo]) -> list[str]:
    """Find potential complexity/design issues."""
    issues = []
    for t in types:
        if len(t.fields) > 20:
            issues.append(f"Type '{t.name}' has {len(t.fields)} fields — consider splitting")
        for f in t.fields:
            if len(f.args) > 5:
                issues.append(f"Field '{t.name}.{f.name}' has {len(f.args)} args — consider input type")
        if t.kind == "enum" and len(t.values) > 20:
            issues.append(f"Enum '{t.name}' has {len(t.values)} values — may be unwieldy")
    return issues


def format_analysis_markdown(types: list[TypeInfo], stats: SchemaStats) -> str:
    """Format schema analysis as Markdown."""
    lines = [
        "# GraphQL Schema Analysis",
        "",
        f"**Types:** {stats.types} | **Inputs:** {stats.inputs} | **Enums:** {stats.enums}",
        f"**Queries:** {stats.queries} | **Mutations:** {stats.mutations} | **Fields:** {stats.total_fields}",
        "",
    ]

    issues = find_complexity_issues(types)
    if issues:
        lines.append("## ⚠️ Issues")
        for i in issues:
            lines.append(f"- {i}")
        lines.append("")

    unused = find_unused_types(types)
    if unused:
        lines.append(f"## 🔍 Potentially Unused Types: {', '.join(unused)}")
        lines.append("")

    lines.append("## Types")
    for t in types:
        if t.kind == "enum":
            lines.append(f"- **{t.name}** (enum): {', '.join(t.values[:5])}")
        elif t.kind == "union":
            lines.append(f"- **{t.name}** (union): {' | '.join(t.values)}")
        elif t.kind == "scalar":
            lines.append(f"- **{t.name}** (scalar)")
        else:
            impl = f" implements {', '.join(t.implements)}" if t.implements else ""
            lines.append(f"- **{t.name}** ({t.kind}{impl}): {len(t.fields)} fields")

    return "\n".join(lines)
