"""Tests for config-file-merger main.py and config.py — targeting 100% coverage."""
import sys, os, json, pytest, runpy
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.merger import merge_configs, deep_merge


# ── config.py coverage ──────────────────────────────────────────────
def test_config_import():
    """Import config.py to cover its module-level code."""
    import config
    assert hasattr(config, 'Config')


# ── merger.py lines 25-29 (list merge strategies) ───────────────────
def test_list_append_strategy():
    base = {"tags": ["a", "b"]}
    override = {"tags": ["c"]}
    merged, conflicts = deep_merge(base, override, strategy="append")
    assert merged["tags"] == ["a", "b", "c"]
    assert len(conflicts) == 0


def test_list_unique_strategy():
    base = {"tags": ["a", "b"]}
    override = {"tags": ["b", "c"]}
    merged, conflicts = deep_merge(base, override, strategy="unique")
    assert set(merged["tags"]) == {"a", "b", "c"}
    assert len(conflicts) == 0


def test_list_override_strategy():
    base = {"tags": ["a", "b"]}
    override = {"tags": ["c"]}
    merged, conflicts = deep_merge(base, override, strategy="override")
    assert merged["tags"] == ["c"]
    assert len(conflicts) == 1


# ── main.py coverage ────────────────────────────────────────────────
def test_cmd_merge_json_output(tmp_path):
    f1 = tmp_path / "a.json"
    f2 = tmp_path / "b.json"
    f1.write_text(json.dumps({"x": 1}))
    f2.write_text(json.dumps({"y": 2}))

    with patch('sys.argv', ['main', 'merge', str(f1), str(f2)]):
        import main
        from io import StringIO
        captured = StringIO()
        with patch('sys.stdout', captured):
            main.main()
        output = captured.getvalue()
        data = json.loads(output)
        assert data["x"] == 1
        assert data["y"] == 2


def test_cmd_merge_report(tmp_path):
    f1 = tmp_path / "a.json"
    f2 = tmp_path / "b.json"
    f1.write_text(json.dumps({"x": 1}))
    f2.write_text(json.dumps({"x": 2}))

    with patch('sys.argv', ['main', 'merge', str(f1), str(f2), '--report']):
        import main
        from io import StringIO
        captured = StringIO()
        with patch('sys.stdout', captured):
            main.main()
        output = captured.getvalue()
        assert "Config Merge" in output


def test_main_block():
    """Cover if __name__ == '__main__' block."""
    with patch('sys.argv', ['main', 'merge', '/dev/null']), \
         patch('builtins.open', mock_open(read_data='{}')):
        runpy.run_module('main', run_name='__main__', alter_sys=True)
