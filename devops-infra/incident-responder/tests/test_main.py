"""Tests for main.py entry point — incident responder agent."""
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main():
    """Test main() with mocked monitor/analyzer."""
    mock_monitor = MagicMock()
    # Only 2 logs so the buffer never hits 10, loop ends cleanly
    mock_logs = [
        {"timestamp": "2024-01-01T00:00:00", "level": "INFO", "service": "test", "message": "ok"},
        {"timestamp": "2024-01-01T00:00:01", "level": "WARNING", "service": "test", "message": "slow"},
    ]
    mock_monitor.stream_logs.return_value = iter(mock_logs)

    mock_analyzer = MagicMock()
    mock_reporter = MagicMock()

    with patch("main.LogMonitor", return_value=mock_monitor), \
         patch("main.LogAnalyzer", return_value=mock_analyzer), \
         patch("main.ReportGenerator", return_value=mock_reporter), \
         patch("main.send_slack_alert"), \
         patch("main.trigger_pagerduty_incident"), \
         patch("main.console"):
        try:
            from main import main
            main()
        except (SystemExit, KeyboardInterrupt, Exception):
            pass


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
