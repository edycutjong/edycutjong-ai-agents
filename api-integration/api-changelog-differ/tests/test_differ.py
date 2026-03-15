"""Tests for API Changelog Differ."""
import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.differ import diff_specs, format_diff_markdown, Severity

OLD_SPEC = {
    "info": {"version": "1.0.0"},
    "paths": {
        "/users": {
            "get": {"parameters": [], "responses": {"200": {}, "404": {}}},
            "post": {"parameters": [{"name": "name", "required": True, "in": "body"}], "responses": {"201": {}}},
        },
        "/legacy": {"get": {"responses": {"200": {}}}},
    },
    "components": {"schemas": {
        "User": {"properties": {"id": {}, "name": {}, "email": {}}, "required": ["id", "name"]},
    }},
}

NEW_SPEC = {
    "info": {"version": "2.0.0"},
    "paths": {
        "/users": {
            "get": {
                "parameters": [{"name": "limit", "required": True, "in": "query"}],
                "responses": {"200": {}},
                "deprecated": True,
            },
            "post": {"parameters": [{"name": "name", "required": True, "in": "body"}], "responses": {"201": {}}},
        },
        "/users/{id}": {"get": {"responses": {"200": {}}}},
    },
    "components": {"schemas": {
        "User": {"properties": {"id": {}, "name": {}, "avatar": {}}, "required": ["id", "name", "avatar"]},
        "Post": {"properties": {"title": {}, "body": {}}},
    }},
}

def test_detects_removed_endpoint():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    removed = [c for c in r.changes if "/legacy" in c.path and c.change_type == "removed"]
    assert len(removed) == 1
    assert removed[0].severity == Severity.BREAKING

def test_detects_added_endpoint():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    added = [c for c in r.changes if "/users/{id}" in c.path and c.change_type == "added"]
    assert len(added) >= 1

def test_detects_deprecated():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    deprecated = [c for c in r.changes if c.change_type == "deprecated"]
    assert len(deprecated) >= 1

def test_detects_new_required_param():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    breaking_params = [c for c in r.changes if "required parameter" in c.description.lower()]
    assert len(breaking_params) >= 1

def test_detects_removed_response_code():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    removed_resp = [c for c in r.changes if "response code removed" in c.description.lower()]
    assert len(removed_resp) >= 1

def test_detects_schema_property_removed():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    removed = [c for c in r.changes if "email" in c.description.lower()]
    assert len(removed) >= 1

def test_detects_schema_property_added():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    added = [c for c in r.changes if "avatar" in c.description.lower()]
    assert len(added) >= 1

def test_detects_new_schema():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    new_schemas = [c for c in r.changes if "Post" in c.description]
    assert len(new_schemas) >= 1

def test_version_tracking():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    assert r.old_version == "1.0.0"
    assert r.new_version == "2.0.0"

def test_breaking_count():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    assert r.breaking_count >= 2

def test_no_changes_identical():
    r = diff_specs(OLD_SPEC, OLD_SPEC)
    assert len(r.changes) == 0

def test_format_markdown():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    md = format_diff_markdown(r)
    assert "API Changelog" in md
    assert "1.0.0" in md
    assert "2.0.0" in md
    assert "Breaking" in md

def test_to_dict():
    r = diff_specs(OLD_SPEC, NEW_SPEC)
    d = r.to_dict()
    assert "total_changes" in d
    assert "changes" in d

def test_empty_specs():
    r = diff_specs({"paths": {}}, {"paths": {}})
    assert len(r.changes) == 0


def test_diff_endpoint_method_removed():
    """Cover lines 106,108: method removed from endpoint (skip 'parameters')."""
    from agent.differ import diff_specs
    old = {"info": {"version": "1"}, "paths": {"/api": {"get": {}, "post": {}, "parameters": []}}, "components": {"schemas": {}}}
    new = {"info": {"version": "2"}, "paths": {"/api": {"get": {}, "parameters": []}}, "components": {"schemas": {}}}
    r = diff_specs(old, new)
    assert any("Method removed" in c.description for c in r.changes)

def test_diff_endpoint_method_added():
    """Cover lines 117,119: new method added to endpoint (skip 'parameters')."""
    from agent.differ import diff_specs
    old = {"info": {"version": "1"}, "paths": {"/api": {"get": {}, "parameters": []}}, "components": {"schemas": {}}}
    new = {"info": {"version": "2"}, "paths": {"/api": {"get": {}, "put": {}, "parameters": []}}, "components": {"schemas": {}}}
    r = diff_specs(old, new)
    assert any("Method added" in c.description for c in r.changes)

def test_diff_new_optional_param():
    """Cover line 146: new optional parameter."""
    from agent.differ import diff_specs
    old = {"info": {"version": "1"}, "paths": {"/api": {"get": {"parameters": []}}}, "components": {"schemas": {}}}
    new = {"info": {"version": "2"}, "paths": {"/api": {"get": {"parameters": [{"name": "limit", "required": False}]}}}, "components": {"schemas": {}}}
    r = diff_specs(old, new)
    assert any("optional parameter" in c.description for c in r.changes)

def test_diff_param_removed():
    """Cover line 153: parameter removed."""
    from agent.differ import diff_specs
    old = {"info": {"version": "1"}, "paths": {"/api": {"get": {"parameters": [{"name": "page"}]}}}, "components": {"schemas": {}}}
    new = {"info": {"version": "2"}, "paths": {"/api": {"get": {"parameters": []}}}, "components": {"schemas": {}}}
    r = diff_specs(old, new)
    assert any("Parameter removed" in c.description for c in r.changes)

def test_diff_new_response_code():
    """Cover line 163: new response code."""
    from agent.differ import diff_specs
    old = {"info": {"version": "1"}, "paths": {"/api": {"get": {"responses": {"200": {}}}}}, "components": {"schemas": {}}}
    new = {"info": {"version": "2"}, "paths": {"/api": {"get": {"responses": {"200": {}, "404": {}}}}}, "components": {"schemas": {}}}
    r = diff_specs(old, new)
    assert any("New response code" in c.description for c in r.changes)

def test_diff_schema_removed():
    """Cover line 179: schema removed."""
    from agent.differ import diff_specs
    old = {"info": {"version": "1"}, "paths": {}, "components": {"schemas": {"User": {"properties": {"id": {}}}}}}
    new = {"info": {"version": "2"}, "paths": {}, "components": {"schemas": {}}}
    r = diff_specs(old, new)
    assert any("Schema removed" in c.description for c in r.changes)

def test_diff_property_now_required():
    """Cover line 204: property changed to required."""
    from agent.differ import diff_specs
    old = {"info": {"version": "1"}, "paths": {}, "components": {"schemas": {"User": {"properties": {"name": {}}, "required": []}}}}
    new = {"info": {"version": "2"}, "paths": {}, "components": {"schemas": {"User": {"properties": {"name": {}}, "required": ["name"]}}}}
    r = diff_specs(old, new)
    assert any("now required" in c.description for c in r.changes)
