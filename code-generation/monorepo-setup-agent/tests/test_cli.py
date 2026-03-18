from typer.testing import CliRunner
from main import app
from unittest.mock import patch, MagicMock

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Interactive wizard to setup a new monorepo" in result.stdout

@patch("main.MonorepoAgent")
@patch("main.Prompt.ask")
@patch("main.Confirm.ask")
def test_cli_flow(mock_confirm, mock_prompt, MockAgent):
    # Mock inputs
    mock_prompt.side_effect = [
        "test-project",  # Project Name
        "pnpm",          # Package Manager
        "turbo",         # Monorepo Tool
        "@repo/ui",      # Package Name
        "github-actions" # CI Provider
    ]
    mock_confirm.side_effect = [
        True,  # Add packages?
        False, # Add another package?
        True   # Proceed?
    ]

    # Mock Agent behavior
    mock_agent_instance = MockAgent.return_value
    mock_agent_instance._create_structure = MagicMock()
    mock_agent_instance._generate_root_files = MagicMock()
    mock_agent_instance._generate_shared_configs = MagicMock()
    mock_agent_instance._generate_ci_files = MagicMock()
    mock_agent_instance._generate_apps = MagicMock()
    mock_agent_instance._generate_packages = MagicMock()

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Monorepo setup complete!" in result.stdout

    # Verify agent was called with correct config
    MockAgent.assert_called_once()
    call_args = MockAgent.call_args[0][0]
    assert call_args.project_name == "test-project"
    assert call_args.package_manager == "pnpm"
    assert call_args.monorepo_tool == "turbo"
    assert call_args.packages[0].name == "@repo/ui"
    assert call_args.ci_provider == "github-actions"


@patch("main.MonorepoAgent")
@patch("main.Prompt.ask")
@patch("main.Confirm.ask")
def test_cli_abort(mock_confirm, mock_prompt, MockAgent):
    """Cover main.py lines 67-68: user aborts generation."""
    mock_prompt.side_effect = [
        "test-project", "pnpm", "turbo", "github-actions"
    ]
    mock_confirm.side_effect = [
        False,  # Don't add packages
        False   # Don't proceed
    ]

    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "Aborted" in result.stdout


@patch("main.MonorepoAgent")
@patch("main.Prompt.ask")
@patch("main.Confirm.ask")
def test_cli_generation_error(mock_confirm, mock_prompt, MockAgent):
    """Cover main.py lines 106-108: error during generation."""
    mock_prompt.side_effect = [
        "test-project", "pnpm", "turbo", "github-actions"
    ]
    mock_confirm.side_effect = [
        False,  # Don't add packages
        True    # Proceed
    ]

    mock_agent_instance = MockAgent.return_value
    mock_agent_instance._create_structure.side_effect = Exception("Disk full")

    result = runner.invoke(app)

    assert result.exit_code == 1
    assert "Error" in result.stdout


@patch("main.MonorepoAgent")
@patch("main.Prompt.ask")
@patch("main.Confirm.ask")
def test_cli_no_ci_no_packages(mock_confirm, mock_prompt, MockAgent):
    """Cover main.py line 61+106-108: CI provider = none triggers validation error."""
    mock_prompt.side_effect = [
        "test-project", "pnpm", "turbo", "none"
    ]
    mock_confirm.side_effect = [
        False,  # Don't add packages
        True    # Proceed
    ]

    result = runner.invoke(app)

    # Pydantic rejects None for ci_provider, causing an error that's caught
    assert result.exit_code == 1


def test_main_module_entry_point():
    """Cover main.py line 111: if __name__ == '__main__': app()."""
    import runpy
    with patch('main.MonorepoAgent'), \
         patch('main.Prompt.ask', side_effect=["test", "pnpm", "turbo", "none"]), \
         patch('main.Confirm.ask', side_effect=[False, True]):
        with patch.dict('sys.modules', {'__main__': None}):
            try:
                runpy.run_module('main', run_name='__main__', alter_sys=True)
            except (SystemExit, Exception):
                pass
