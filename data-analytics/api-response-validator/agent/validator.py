"""API response validator — validate API responses against expected schemas."""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field

@dataclass
class ValidationRule:
    field: str
    expected_type: str = ""  # string, number, boolean, array, object, null
    required: bool = False
    min_length: int = 0
    max_length: int = 0
    pattern: str = ""

@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    fields_checked: int = 0
    status_code: int = 0
    response_time_ms: float = 0

TYPE_MAP = {"string": str, "number": (int, float), "boolean": bool, "array": list, "object": dict}

def validate_type(value, expected_type: str) -> bool:
    if expected_type == "null": return value is None
    return isinstance(value, TYPE_MAP.get(expected_type, object))

def validate_response(data: dict, rules: list[ValidationRule], status_code: int = 200) -> ValidationResult:
    r = ValidationResult(status_code=status_code)
    if status_code >= 400:
        r.warnings.append(f"HTTP status {status_code} indicates an error")
    for rule in rules:
        r.fields_checked += 1
        # Check field existence
        value = data.get(rule.field)
        if value is None and rule.field not in data:
            if rule.required:
                r.is_valid = False
                r.errors.append(f"Required field '{rule.field}' is missing")
            continue
        # Check type
        if rule.expected_type and not validate_type(value, rule.expected_type):
            r.is_valid = False
            actual = type(value).__name__
            r.errors.append(f"Field '{rule.field}': expected {rule.expected_type}, got {actual}")
            continue
        # Check string constraints
        if isinstance(value, str):
            if rule.min_length and len(value) < rule.min_length:
                r.errors.append(f"Field '{rule.field}': length {len(value)} < min {rule.min_length}")
                r.is_valid = False
            if rule.max_length and len(value) > rule.max_length:
                r.errors.append(f"Field '{rule.field}': length {len(value)} > max {rule.max_length}")
                r.is_valid = False
            if rule.pattern and not re.match(rule.pattern, value):
                r.errors.append(f"Field '{rule.field}': does not match pattern '{rule.pattern}'")
                r.is_valid = False
    return r

def create_rules_from_sample(data: dict) -> list[ValidationRule]:
    rules = []
    for key, value in data.items():
        rule = ValidationRule(field=key, required=True)
        if isinstance(value, str): rule.expected_type = "string"
        elif isinstance(value, bool): rule.expected_type = "boolean"
        elif isinstance(value, (int, float)): rule.expected_type = "number"
        elif isinstance(value, list): rule.expected_type = "array"
        elif isinstance(value, dict): rule.expected_type = "object"
        elif value is None: rule.expected_type = "null"
        rules.append(rule)
    return rules

def format_result_markdown(r: ValidationResult) -> str:
    emoji = "✅" if r.is_valid else "❌"
    lines = [f"## API Response Validation {emoji}", f"**Valid:** {r.is_valid} | **Fields Checked:** {r.fields_checked} | **Status:** {r.status_code}", ""]
    if r.errors:
        lines.append("### Errors")
        for e in r.errors: lines.append(f"- ❌ {e}")
    if r.warnings:
        lines.append("### Warnings")
        for w in r.warnings: lines.append(f"- ⚠️ {w}")
    if not r.errors and not r.warnings:
        lines.append("✅ All validations passed!")
    return "\n".join(lines)
