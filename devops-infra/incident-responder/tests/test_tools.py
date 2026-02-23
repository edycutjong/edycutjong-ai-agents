import pytest
from unittest.mock import patch
from agent.tools import send_slack_alert, trigger_pagerduty_incident

@patch("requests.post")
def test_send_slack_alert_mock(mock_post):
    mock_post.return_value.status_code = 200

    success = send_slack_alert("Test Alert", webhook_url="https://hooks.slack.com/services/XXX")
    assert success
    mock_post.assert_called_once()

def test_send_slack_alert_no_url():
    # Should print to console and return True (simulation)
    success = send_slack_alert("Test Alert")
    assert success

def test_trigger_pagerduty_incident_no_key():
    # Should print to console and return True (simulation)
    success = trigger_pagerduty_incident("Test Incident", "HIGH")
    assert success
