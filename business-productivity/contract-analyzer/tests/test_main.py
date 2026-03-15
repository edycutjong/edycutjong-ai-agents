"""Tests for Contract Analyzer CLI and Config."""
import sys, os, json, pytest
from unittest.mock import patch, mock_open
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from main import main, cmd_analyze

SAMPLE_TEXT = """
SERVICE AGREEMENT
This Agreement is entered into as of January 15, 2026.
1. PAYMENT TERMS - Client shall pay within Net 30 days.
2. TERMINATION - Either party may terminate with 30 days notice.
"""


def test_config_class():
    """Cover config.py: Config class exists."""
    assert Config is not None


def test_cmd_analyze_file(tmp_path):
    """Cover main.py cmd_analyze with file input."""
    contract_file = tmp_path / "contract.txt"
    contract_file.write_text(SAMPLE_TEXT)

    args = type('Args', (), {'file': str(contract_file), 'json': False})()
    # Should not raise
    cmd_analyze(args)


def test_cmd_analyze_json(tmp_path, capsys):
    """Cover main.py cmd_analyze with --json flag."""
    contract_file = tmp_path / "contract.txt"
    contract_file.write_text(SAMPLE_TEXT)

    args = type('Args', (), {'file': str(contract_file), 'json': True})()
    cmd_analyze(args)

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert "risk_score" in result


def test_cmd_analyze_stdin(monkeypatch):
    """Cover main.py cmd_analyze with stdin input."""
    monkeypatch.setattr('sys.stdin', type('IO', (), {'read': lambda self: SAMPLE_TEXT})())
    args = type('Args', (), {'file': '-', 'json': False})()
    cmd_analyze(args)


def test_main_cli(tmp_path):
    """Cover main.py main() function."""
    contract_file = tmp_path / "contract.txt"
    contract_file.write_text(SAMPLE_TEXT)

    with patch('sys.argv', ['main.py', 'analyze', str(contract_file)]):
        main()


def test_main_cli_json(tmp_path, capsys):
    """Cover main.py main() with --json."""
    contract_file = tmp_path / "contract.txt"
    contract_file.write_text(SAMPLE_TEXT)

    with patch('sys.argv', ['main.py', 'analyze', str(contract_file), '--json']):
        main()

    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert "clauses" in result
