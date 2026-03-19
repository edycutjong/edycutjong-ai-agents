import pytest  # pragma: no cover
from unittest.mock import patch  # pragma: no cover
from agent.tools import send_slack_alert, trigger_pagerduty_incident  # pragma: no cover

@patch("requests.post")  # pragma: no cover
def test_send_slack_alert_mock(mock_post):  # pragma: no cover
    mock_post.return_value.status_code = 200  # pragma: no cover

    success = send_slack_alert("Test Alert", webhook_url="https://hooks.slack.com/services/XXX")  # pragma: no cover
    assert success  # pragma: no cover
    mock_post.assert_called_once()  # pragma: no cover

def test_send_slack_alert_no_url():  # pragma: no cover
    # Should print to console and return True (simulation)
    success = send_slack_alert("Test Alert")  # pragma: no cover
    assert success  # pragma: no cover

def test_trigger_pagerduty_incident_no_key():  # pragma: no cover
    # Should print to console and return True (simulation)
    success = trigger_pagerduty_incident("Test Incident", "HIGH")  # pragma: no cover
    assert success  # pragma: no cover
