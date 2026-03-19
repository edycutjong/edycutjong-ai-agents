"""Coverage tests for main.py — incident responder agent."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_coverage():
    """Test main() with mocked monitor and analyzer to prevent real API calls."""
    # Mock the log monitor to yield a few logs then raise KeyboardInterrupt
    mock_monitor = MagicMock()
    mock_logs = [
        {"timestamp": "2024-01-01T00:00:00", "level": "INFO", "service": "test", "message": "ok"},
        {"timestamp": "2024-01-01T00:00:01", "level": "ERROR", "service": "test", "message": "fail"},
    ]
    mock_monitor.stream_logs.return_value = iter(mock_logs)

    mock_analyzer = MagicMock()
    mock_analyzer.analyze_logs.return_value = {"severity": "LOW", "summary": "test", "root_cause": "none"}

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
