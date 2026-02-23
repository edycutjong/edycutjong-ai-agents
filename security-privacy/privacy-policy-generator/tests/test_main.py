import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Ensure imports work
sys.path.append(str(Path(__file__).parents[1]))

from main import run_scan, run_generate, main
from rich.console import Console
from agent.generator import PolicyGenerator
from config import Config

def test_run_scan_cli(tmp_path):
    """Test CLI scan function."""
    d = tmp_path / "test_scan"
    d.mkdir()
    (d / "test.py").write_text("email = 'test'")

    mock_console = MagicMock(spec=Console)

    results = run_scan(str(d), mock_console)

    assert results["files_scanned"] == 1
    assert "email" in results["pii"]
    mock_console.print.assert_called()

def test_run_scan_empty(tmp_path):
    """Test CLI scan on empty dir."""
    mock_console = MagicMock(spec=Console)
    results = run_scan(str(tmp_path), mock_console)

    assert results["files_scanned"] == 0
    mock_console.print.assert_called()

@patch("main.PolicyGenerator")
@patch("main.Config")
def test_run_generate_cli(mock_config, mock_generator_cls, tmp_path):
    """Test CLI generate function."""
    d = tmp_path / "test_gen"
    d.mkdir()
    (d / "test.py").write_text("email = 'test'")

    mock_config.OPENAI_API_KEY = "test-key"
    mock_config.MODEL_NAME = "gpt-4-turbo"

    mock_gen_instance = MagicMock()
    mock_gen_instance.generate_policy.return_value = "# Policy Content"
    mock_generator_cls.return_value = mock_gen_instance

    mock_console = MagicMock(spec=Console)

    output_dir = tmp_path / "output"

    run_generate(str(d), "gdpr", str(output_dir), mock_console)

    assert (output_dir / "privacy_policy_gdpr.md").exists()
    assert (output_dir / "privacy_policy_gdpr.html").exists()
    mock_gen_instance.generate_policy.assert_called()

@patch("main.Config")
def test_run_generate_no_key(mock_config, tmp_path):
    """Test CLI generate without API key."""
    mock_config.OPENAI_API_KEY = None
    mock_console = MagicMock(spec=Console)

    run_generate(str(tmp_path), "gdpr", "output", mock_console)

    # Check for error message
    args, _ = mock_console.print.call_args
    assert "Error" in str(args[0])

@patch("argparse.ArgumentParser.parse_args")
@patch("main.run_scan")
def test_main_scan(mock_run_scan, mock_args):
    """Test main entry point for scan."""
    mock_args.return_value = MagicMock(command="scan", directory=".")

    # We need to mock Console inside main, or let it run (it just prints).
    # Since Console is instantiated inside main, we can patch 'main.Console'.
    with patch("main.Console"):
        main()
        mock_run_scan.assert_called()

@patch("argparse.ArgumentParser.parse_args")
@patch("main.run_generate")
def test_main_generate(mock_run_gen, mock_args):
    """Test main entry point for generate."""
    mock_args.return_value = MagicMock(command="generate", directory=".", type="gdpr", output="output")

    with patch("main.Console"):
        main()
        mock_run_gen.assert_called()
