import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.parser import UIParser, UIElement
from agent.test_generator import TestGenerator
from agent.runner import TestRunner

# --- Test UIParser ---
def test_ui_parser_buttons():
    html = """
    <html>
        <body>
            <button id="submit-btn" class="primary">Submit</button>
            <input type="text" id="username" placeholder="Enter User">
            <a href="/login">Login</a>
        </body>
    </html>
    """
    parser = UIParser()
    elements = parser.parse_html(html)

    assert len(elements) == 3

    btn = next(e for e in elements if e.tag == "button")
    assert btn.id == "submit-btn"
    assert btn.text == "Submit"

    inp = next(e for e in elements if e.tag == "input")
    assert inp.id == "username"
    assert "Placeholder: Enter User" in inp.text

    link = next(e for e in elements if e.tag == "a")
    assert link.attrs['href'] == "/login"

# --- Test TestGenerator ---
@patch("agent.test_generator.ChatOpenAI")
def test_generator_init(MockChatOpenAI):
    # Verify initialization with key
    generator = TestGenerator(api_key="fake-key")
    assert generator.llm is not None
    MockChatOpenAI.assert_called_with(api_key="fake-key", model="gpt-4-turbo", temperature=0.7)

@patch.dict(os.environ, {"OPENAI_API_KEY": ""})
def test_generator_no_key():
    # Verify fallback behavior when no key is provided
    generator = TestGenerator(api_key=None)
    assert generator.llm is None

    scenarios = generator.generate_scenarios([{"tag": "button"}])
    assert len(scenarios) > 0
    assert "Mock Scenario" in scenarios[0]

    code = generator.generate_playwright_code([], "http://test.com", "<html></html>")
    assert "def test_page_title" in code

    healing = generator.self_heal("error", "code")
    assert "Mock fix" in healing

# --- Test TestRunner ---
@patch("os.path.exists")
@patch("subprocess.run")
def test_runner_success(mock_run, mock_exists):
    # Mock file exists
    mock_exists.return_value = True

    # Mock successful run
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "=== 2 passed in 0.12s ==="
    mock_result.stderr = ""
    mock_run.return_value = mock_result

    # Test headless (default)
    runner = TestRunner(headless=True)
    result = runner.run_tests("dummy_test.py")

    assert result["success"] is True
    assert result["passed"] == 2
    mock_run.assert_called_with(["pytest", "dummy_test.py", "--verbose"], capture_output=True, text=True, check=False)

    # Test headed
    runner_headed = TestRunner(headless=False)
    runner_headed.run_tests("dummy_test.py")
    mock_run.assert_called_with(["pytest", "dummy_test.py", "--verbose", "--headed"], capture_output=True, text=True, check=False)

@patch("os.path.exists")
@patch("subprocess.run")
def test_runner_failure(mock_run, mock_exists):
    # Mock file exists
    mock_exists.return_value = True

    # Mock failed run
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = "=== 1 failed, 1 passed in 0.12s ==="
    mock_result.stderr = ""
    mock_run.return_value = mock_result

    runner = TestRunner()
    result = runner.run_tests("dummy_test.py")

    assert result["success"] is False # pytest returns 1 if tests fail
    assert result["passed"] == 1
    assert result["failed"] == 1
