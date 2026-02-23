import sys
import os
import pytest

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.diff_engine import detect_breaking_changes, ChangeType, APIChange

def test_no_changes():
    spec = {"paths": {"/a": {"get": {}}}}
    assert detect_breaking_changes(spec, spec) == []

def test_removed_path():
    old = {"paths": {"/a": {"get": {}}}}
    new = {"paths": {}}
    changes = detect_breaking_changes(old, new)
    # Expect 1 change
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.BREAKING
    assert "Path removed: /a" in changes[0].description

def test_removed_operation():
    old = {"paths": {"/a": {"get": {}, "post": {}}}}
    new = {"paths": {"/a": {"get": {}}}}
    changes = detect_breaking_changes(old, new)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.BREAKING
    assert "Operation POST removed" in changes[0].description

def test_added_required_param():
    old = {"paths": {"/a": {"get": {"parameters": []}}}}
    new = {"paths": {"/a": {"get": {"parameters": [{"name": "p", "required": True}]}}}}
    changes = detect_breaking_changes(old, new)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.BREAKING
    assert "New required parameter 'p' added" in changes[0].description

def test_made_param_required():
    old = {"paths": {"/a": {"get": {"parameters": [{"name": "p", "required": False}]}}}}
    new = {"paths": {"/a": {"get": {"parameters": [{"name": "p", "required": True}]}}}}
    changes = detect_breaking_changes(old, new)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.BREAKING
    assert "Parameter 'p' became required" in changes[0].description

def test_param_type_changed():
    old = {"paths": {"/a": {"get": {"parameters": [{"name": "p", "schema": {"type": "string"}}]}}}}
    new = {"paths": {"/a": {"get": {"parameters": [{"name": "p", "schema": {"type": "integer"}}]}}}}
    changes = detect_breaking_changes(old, new)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.BREAKING
    assert "type changed from string to integer" in changes[0].description

def test_response_type_change_with_int_keys():
    # Test with integer status code keys (common in YAML parsing)
    old = {
        "paths": {
            "/a": {
                "get": {
                    "responses": {
                        200: {
                            "content": {
                                "application/json": {
                                    "schema": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    new = {
        "paths": {
            "/a": {
                "get": {
                    "responses": {
                        200: {
                            "content": {
                                "application/json": {
                                    "schema": {"type": "integer"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    changes = detect_breaking_changes(old, new)
    assert len(changes) == 1
    assert changes[0].change_type == ChangeType.BREAKING
    assert "Response 200 type changed" in changes[0].description

def test_ignore_refs_in_params():
    # Parameters with $ref don't have 'name' immediately inside. Should not crash.
    old = {
        "paths": {
            "/a": {
                "get": {
                    "parameters": [{"$ref": "#/components/parameters/Limit"}]
                }
            }
        }
    }
    new = {
        "paths": {
            "/a": {
                "get": {
                    "parameters": [{"$ref": "#/components/parameters/Limit"}]
                }
            }
        }
    }
    changes = detect_breaking_changes(old, new)
    assert len(changes) == 0
