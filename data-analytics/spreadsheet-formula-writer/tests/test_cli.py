import pytest
from typer.testing import CliRunner
from unittest.mock import MagicMock
from agent.models import FormulaResponse

# Import app from main
# We need to ensure sys.path is correct for this import to work
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from main import app

runner = CliRunner()

def test_cli_success(mocker):
    # Mock FormulaWriterAgent in main module
    mock_agent_cls = mocker.patch("main.FormulaWriterAgent")
    mock_agent_instance = mock_agent_cls.return_value

    mock_response = FormulaResponse(
        formula="=SUM(A1:A10)",
        explanation="Sums values in A1 to A10.",
        alternatives=["=SUM(A:A)"],
        examples=["If A1=1..."]
    )
    mock_agent_instance.generate_formula.return_value = mock_response

    result = runner.invoke(app, ["Sum column A"])

    assert result.exit_code == 0
    assert "=SUM(A1:A10)" in result.stdout
    assert "Sums values in A1 to A10." in result.stdout
    assert "Alternative Approaches" in result.stdout
    assert "Usage Examples" in result.stdout

def test_cli_error(mocker):
    # Mock FormulaWriterAgent to raise exception
    mock_agent_cls = mocker.patch("main.FormulaWriterAgent")
    mock_agent_instance = mock_agent_cls.return_value
    mock_agent_instance.generate_formula.side_effect = RuntimeError("API Error")

    result = runner.invoke(app, ["Sum column A"])

    assert result.exit_code == 1
    assert "Error" in result.stdout
    assert "API Error" in result.stdout

def test_cli_options(mocker):
    # Mock FormulaWriterAgent
    mock_agent_cls = mocker.patch("main.FormulaWriterAgent")
    mock_agent_instance = mock_agent_cls.return_value
    mock_agent_instance.generate_formula.return_value = FormulaResponse(
        formula="=GOOGLEFINANCE()",
        explanation="Foo",
        alternatives=[],
        examples=[]
    )

    result = runner.invoke(app, ["Stock price", "--target", "Google Sheets", "--model", "gpt-3.5-turbo"])

    assert result.exit_code == 0
    mock_agent_cls.assert_called_with(model_name="gpt-3.5-turbo")
    mock_agent_instance.generate_formula.assert_called_with("Stock price", target_application="Google Sheets")

def test_interactive_mode(mocker):
    # Mock Prompt.ask
    mock_prompt = mocker.patch("main.Prompt.ask")
    # Simulate a user flow: query -> result -> exit
    mock_prompt.side_effect = ["Sum column A", "/exit"]

    # Mock Agent
    mock_agent_cls = mocker.patch("main.FormulaWriterAgent")
    mock_agent_instance = mock_agent_cls.return_value
    mock_agent_instance.generate_formula.return_value = FormulaResponse(
        formula="=SUM(A:A)",
        explanation="Sums column A",
        alternatives=[],
        examples=[]
    )

    result = runner.invoke(app, []) # No query, triggers interactive mode

    assert result.exit_code == 0
    assert "Welcome" in result.stdout
    assert "Generated Formula" in result.stdout
    assert "=SUM(A:A)" in result.stdout
    assert "Goodbye!" in result.stdout
