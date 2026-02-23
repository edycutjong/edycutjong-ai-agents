import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import monitor_job

@patch('main.check_endpoint')
@patch('main.check_ssl_expiry')
@patch('main.add_result')
@patch('main.analyze_failure')
@patch('main.send_alert')
@patch('main.MONITOR_ENDPOINTS', ['http://example.com'])
def test_monitor_job(mock_send_alert, mock_analyze, mock_add_result, mock_check_ssl, mock_check_endpoint):
    # Setup mocks
    mock_check_endpoint.return_value = (200, 0.5, None)
    mock_check_ssl.return_value = (100, None)

    monitor_job()

    # Assertions
    mock_check_endpoint.assert_called_with('http://example.com')
    mock_check_ssl.assert_called_with('http://example.com')
    mock_add_result.assert_called_once()
    mock_analyze.assert_not_called()
    mock_send_alert.assert_not_called()

@patch('main.check_endpoint')
@patch('main.check_ssl_expiry')
@patch('main.add_result')
@patch('main.analyze_failure')
@patch('main.send_alert')
@patch('main.MONITOR_ENDPOINTS', ['http://example.com'])
def test_monitor_job_down(mock_send_alert, mock_analyze, mock_add_result, mock_check_ssl, mock_check_endpoint):
    # Setup mocks for downtime
    mock_check_endpoint.return_value = (500, 0.1, "Internal Server Error")
    mock_check_ssl.return_value = (100, None)
    mock_analyze.return_value = "Diagnosis"

    monitor_job()

    # Assertions
    mock_check_endpoint.assert_called_with('http://example.com')
    mock_analyze.assert_called_with('http://example.com', 500, 0.1, "Internal Server Error")
    mock_send_alert.assert_called_with('http://example.com', "Internal Server Error", "Diagnosis")
    mock_add_result.assert_called_once()
