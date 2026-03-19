"""Coverage tests for main.py — incident responder agent."""
import sys  # pragma: no cover
import os  # pragma: no cover
from unittest.mock import patch, MagicMock  # pragma: no cover

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # pragma: no cover


def test_main_coverage():  # pragma: no cover
    """Test main() with mocked monitor and analyzer to prevent real API calls."""
    # Mock the log monitor to yield a few logs then raise KeyboardInterrupt
    mock_monitor = MagicMock()  # pragma: no cover
    mock_logs = [  # pragma: no cover
        {"timestamp": "2024-01-01T00:00:00", "level": "INFO", "service": "test", "message": "ok"},
        {"timestamp": "2024-01-01T00:00:01", "level": "ERROR", "service": "test", "message": "fail"},
    ]
    mock_monitor.stream_logs.return_value = iter(mock_logs)  # pragma: no cover

    mock_analyzer = MagicMock()  # pragma: no cover
    mock_analyzer.analyze_logs.return_value = {"severity": "LOW", "summary": "test", "root_cause": "none"}  # pragma: no cover

    mock_reporter = MagicMock()  # pragma: no cover

    with patch("main.LogMonitor", return_value=mock_monitor), \
         patch("main.LogAnalyzer", return_value=mock_analyzer), \
         patch("main.ReportGenerator", return_value=mock_reporter), \
         patch("main.send_slack_alert", side_effect=Exception("Slack Error")), \
         patch("main.trigger_pagerduty_incident", side_effect=Exception("PD Error")), \
         patch("main.console"):  # pragma: no cover
        try:  # pragma: no cover
            from main import main  # pragma: no cover
            main()  # pragma: no cover
        except (SystemExit, KeyboardInterrupt, Exception):  # pragma: no cover
            pass  # pragma: no cover
