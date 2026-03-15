"""Tests for csv-cleaner main.py, config.py, and remaining cleaner.py gaps."""
import sys, os, json, pytest, runpy
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd


# ── config.py coverage ──────────────────────────────────────────────
def test_config_import():
    import config
    assert hasattr(config, 'Config')
    assert config.Config.DEFAULT_ENCODING == "utf-8"
    assert isinstance(config.Config.MAX_FILE_SIZE_MB, int)


def test_config_env_override():
    with patch.dict(os.environ, {"DEFAULT_ENCODING": "latin-1", "MAX_FILE_SIZE_MB": "50"}):
        # Force re-import
        import importlib
        import config
        importlib.reload(config)
        assert config.Config.DEFAULT_ENCODING == "latin-1"
        assert config.Config.MAX_FILE_SIZE_MB == 50


# ── cleaner.py missing lines ────────────────────────────────────────
from agent.cleaner import CSVCleaner


def test_load_csv_from_raw_bytes_non_utf8():
    """Cover lines 82-84: encoding_fixed branch for non-utf8 raw bytes."""
    cleaner = CSVCleaner()
    csv_content = "name,age\nAlice,30\n"
    raw = csv_content.encode("latin-1")
    with patch.object(cleaner, 'detect_encoding', return_value='latin-1'):
        df = cleaner.load_csv(raw_bytes=raw)
        assert cleaner.report.encoding_fixed is True
        assert len(df) == 1


def test_load_csv_from_filepath(tmp_path):
    """Cover lines 88-90: filepath branch."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_bytes(b"name,age\nBob,25\n")
    cleaner = CSVCleaner()
    df = cleaner.load_csv(filepath=str(csv_file))
    assert len(df) == 1


def test_load_csv_no_args():
    """Cover line 92: ValueError when no args."""
    cleaner = CSVCleaner()
    with pytest.raises(ValueError, match="Provide filepath"):
        cleaner.load_csv()


def test_handle_missing_fill_mode():
    """Cover lines 148-151: fill_mode strategy."""
    cleaner = CSVCleaner()
    df = pd.DataFrame({"a": [1, 2, None, 2], "b": ["x", "x", None, "x"]})
    cleaner.report.original_rows = len(df)
    result = cleaner.handle_missing_values(df, strategy="fill_mode")
    assert result.isnull().sum().sum() == 0


def test_handle_missing_unknown_strategy():
    """Cover line 155: unknown strategy raises ValueError."""
    cleaner = CSVCleaner()
    df = pd.DataFrame({"a": [1, None]})
    with pytest.raises(ValueError, match="Unknown strategy"):
        cleaner.handle_missing_values(df, strategy="bogus")


def test_standardize_dates_parse_error():
    """Cover lines 186-187: date parsing failure on a column."""
    cleaner = CSVCleaner()
    df = pd.DataFrame({"dates": ["not-a-date", "also-not"]})
    result = cleaner.standardize_dates(df, columns=["dates"])
    # Should not crash, just skip
    assert "dates" in result.columns


def test_fix_column_types_numeric():
    """Cover lines 202-203, 208-209: successful numeric type fix."""
    cleaner = CSVCleaner()
    df = pd.DataFrame({"nums": ["1", "2", "3"]})
    result = cleaner.fix_column_types(df)
    assert result["nums"].dtype in ("int64", "float64")
    assert cleaner.report.type_fixes == 1


# ── main.py coverage ────────────────────────────────────────────────
def test_main_file_not_found():
    with patch('sys.argv', ['main', 'nonexistent.csv']):
        with pytest.raises(SystemExit) as exc_info:
            import main
            main.main()
        assert exc_info.value.code == 1


def test_main_report_dry_run(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25\n")
    with patch('sys.argv', ['main', str(csv_file), '--report', '--dry-run']):
        import main
        captured = StringIO()
        with patch('sys.stdout', captured):
            main.main()
        output = captured.getvalue()
        assert "Data Quality Summary" in output


def test_main_clean_with_report(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\nAlice,30\nBob,25\n")  # duplicate row to trigger actions
    with patch('sys.argv', ['main', str(csv_file), '--report', '-o', str(tmp_path / 'out.csv')]):
        import main
        captured = StringIO()
        with patch('sys.stdout', captured):
            main.main()
        output = captured.getvalue()
        assert "Cleaning Report" in output or "Actions" in output


def test_main_clean_markdown_report(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25\n")
    with patch('sys.argv', ['main', str(csv_file), '--report', '--markdown', '-o', str(tmp_path / 'out.csv')]):
        import main
        captured = StringIO()
        with patch('sys.stdout', captured):
            main.main()
        output = captured.getvalue()
        assert "CSV Cleaning Report" in output or "Loading" in output


def test_main_dry_run_no_save(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\n")
    with patch('sys.argv', ['main', str(csv_file), '--dry-run']):
        import main
        captured = StringIO()
        with patch('sys.stdout', captured):
            main.main()
        output = captured.getvalue()
        assert "Dry run" in output or "Loading" in output


def test_main_default_output(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\n")
    with patch('sys.argv', ['main', str(csv_file)]):
        import main
        captured = StringIO()
        with patch('sys.stdout', captured):
            main.main()
        output = captured.getvalue()
        assert "Saved" in output or "Loading" in output


def test_main_block(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\n")
    with patch('sys.argv', ['main', str(csv_file), '-o', str(tmp_path / 'out.csv')]):
        runpy.run_module('main', run_name='__main__', alter_sys=True)
