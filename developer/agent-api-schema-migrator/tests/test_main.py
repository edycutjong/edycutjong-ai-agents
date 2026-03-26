import json
import os
import sys
import pytest
from unittest.mock import patch
from main import run, compare_schemas, find_removed_fields, find_added_fields, find_type_changes, generate_migration_guide, load_schema, main


def test_run():
    assert "API Schema Migrator" in run("test")


def test_no_changes():
    result = compare_schemas({"a": 1}, {"a": 1})
    assert result["total_changes"] == 0
    assert not result["migration_required"]


def test_removed_field():
    result = compare_schemas({"a": 1, "b": 2}, {"a": 1})
    assert result["breaking_changes"] == 1
    assert result["migration_required"]


def test_added_field():
    result = compare_schemas({"a": 1}, {"a": 1, "b": 2})
    assert result["total_changes"] == 1
    assert not result["migration_required"]


def test_type_change():
    result = compare_schemas({"a": "str"}, {"a": 123})
    assert result["breaking_changes"] == 1


def test_nested_removal():
    old = {"user": {"name": "x", "age": 1}}
    new = {"user": {"name": "x"}}
    removed = find_removed_fields(old, new)
    assert len(removed) == 1
    assert removed[0]["path"] == "user.age"


def test_migration_guide_safe():
    result = {"migration_required": False, "breaking_changes": 0, "changes": [], "total_changes": 0}
    guide = generate_migration_guide(result)
    assert "safe to upgrade" in guide.lower()


def test_migration_guide_breaking():
    result = {"migration_required": True, "breaking_changes": 1, "total_changes": 1,
              "changes": [{"type": "REMOVED", "path": "name", "severity": "BREAKING"}]}
    guide = generate_migration_guide(result)
    assert "REMOVED" in guide


def test_load_schema_string():
    assert load_schema('{"a": 1}') == {"a": 1}


def test_load_schema_file(tmp_path):
    p = tmp_path / "test.json"
    p.write_text('{"a": 1}')
    assert load_schema(str(p)) == {"a": 1}


def test_nested_addition():
    old = {"user": {"name": "x"}}
    new = {"user": {"name": "x", "age": 1}}
    additions = find_added_fields(old, new)
    assert len(additions) == 1
    assert additions[0]["path"] == "user.age"


def test_nested_type_change():
    old = {"user": {"age": "1"}}
    new = {"user": {"age": 1}}
    changes = find_type_changes(old, new)
    assert len(changes) == 1
    assert changes[0]["path"] == "user.age"


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


@patch("sys.argv", ["main.py", '{"a": 1}', '{"b": 2}'])
def test_main_with_args(capsys):
    main()
    captured = capsys.readouterr()
    assert "REMOVED" in captured.out or "ADDED" in captured.out
