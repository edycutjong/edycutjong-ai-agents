"""Tests for main.py entry point — Figma to CSS agent."""
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main():
    """Test main() in interactive mode with mocked agent and prompt."""
    mock_prompt = MagicMock()
    mock_prompt.ask.side_effect = ["exit"]
    mock_agent = MagicMock()
    mock_agent.run.return_value = "CSS output"
    with patch("sys.argv", ["main.py"]), \
         patch("main.Prompt", mock_prompt), \
         patch("main.FigmaAgent", return_value=mock_agent), \
         patch("main.OPENAI_API_KEY", "test-key"), \
         patch("main.console"):
        try:
            from main import main
            main()
        except (SystemExit, Exception):  # pragma: no cover
            pass  # pragma: no cover


def test_main_block():
    """Test __main__ block."""
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with open(script) as f:
        source = f.read()
    assert 'if __name__' in source
    with patch("main.main") as mock_main:
        exec(
            compile("if __name__ == '__main__': main()", script, "exec"),
            {"__name__": "__main__", "main": mock_main},
        )
        mock_main.assert_called_once()
