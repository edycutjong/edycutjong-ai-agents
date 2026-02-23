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
