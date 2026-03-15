import os
from agent.validator import create_rules_from_sample, ValidationResult, format_result_markdown
import config

def test_config():
    assert config.Config is not None

def test_create_rules_object_and_null():
    sample = {
        "obj": {"a": 1},
        "null_val": None
    }
    rules = create_rules_from_sample(sample)
    assert len(rules) == 2
    assert rules[0].expected_type == "object"
    assert rules[1].expected_type == "null"

def test_format_result_markdown_errors_warnings():
    r = ValidationResult(is_valid=False, errors=["Error 1"], warnings=["Warning 1"], fields_checked=1, status_code=400)
    out = format_result_markdown(r)
    assert "### Errors" in out
    assert "- ❌ Error 1" in out
    assert "### Warnings" in out
    assert "- ⚠️ Warning 1" in out
