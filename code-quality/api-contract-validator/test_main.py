"""Tests for API Contract Validator agent."""
import pytest
from main import run, validate_json_schema_basic


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "API Contract Validator" in result


class TestValidateJsonSchemaBasic:
    def test_valid_data_no_errors(self):
        schema = {"required": ["name"], "properties": {"name": {"type": "string"}}}
        data = {"name": "test"}
        errors = validate_json_schema_basic(data, schema)
        assert errors == []

    def test_missing_required_field(self):
        schema = {"required": ["name", "email"], "properties": {}}
        data = {"name": "test"}
        errors = validate_json_schema_basic(data, schema)
        assert any("email" in e for e in errors)

    def test_wrong_type_string(self):
        schema = {"required": [], "properties": {"age": {"type": "integer"}}}
        data = {"age": "not_a_number"}
        errors = validate_json_schema_basic(data, schema)
        assert any("age" in e for e in errors)

    def test_wrong_type_boolean(self):
        schema = {"required": [], "properties": {"active": {"type": "boolean"}}}
        data = {"active": "yes"}
        errors = validate_json_schema_basic(data, schema)
        assert any("active" in e for e in errors)

    def test_correct_types_no_errors(self):
        schema = {"required": [], "properties": {
            "name": {"type": "string"},
            "count": {"type": "integer"},
            "tags": {"type": "array"},
        }}
        data = {"name": "test", "count": 5, "tags": ["a"]}
        errors = validate_json_schema_basic(data, schema)
        assert errors == []

    def test_empty_schema_no_errors(self):
        errors = validate_json_schema_basic({"any": "data"}, {})
        assert errors == []
