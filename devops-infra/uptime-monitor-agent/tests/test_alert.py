import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.alert import send_email_alert, send_webhook_alert, send_alert

@patch('agent.alert.smtplib.SMTP')
def test_send_email_alert(mock_smtp):
    mock_server = Mock()
    mock_smtp.return_value = mock_server

    # Mock environment variables
    with patch('agent.alert.EMAIL_SENDER', 'sender@example.com'), \
         patch('agent.alert.EMAIL_PASSWORD', 'pass'), \
         patch('agent.alert.EMAIL_RECIPIENT', 'recipient@example.com'):

        success = send_email_alert("Subject", "Body")
        assert success is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with('sender@example.com', 'pass')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

@patch('agent.alert.requests.post')
def test_send_webhook_alert(mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    with patch('agent.alert.WEBHOOK_URL', 'http://webhook.url'):
        success = send_webhook_alert("Message")
        assert success is True
        mock_post.assert_called_with('http://webhook.url', json={"content": "Message"})

@patch('agent.alert.send_email_alert')
@patch('agent.alert.send_webhook_alert')
def test_send_alert(mock_webhook, mock_email):
    mock_email.return_value = True
    mock_webhook.return_value = True

    send_alert("http://example.com", "Error", "Diagnosis")

    mock_email.assert_called_once()
    mock_webhook.assert_called_once()
