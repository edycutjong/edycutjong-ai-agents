import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import monitor_job, main

@patch('main.check_endpoint')
@patch('main.check_ssl_expiry')
@patch('main.add_result')
@patch('main.analyze_failure')
@patch('main.send_alert')
@patch('main.MONITOR_ENDPOINTS', ['http://example.com'])
def test_monitor_job(mock_send_alert, mock_analyze, mock_add_result, mock_check_ssl, mock_check_endpoint):
    mock_check_endpoint.return_value = (200, 0.5, None)
    mock_check_ssl.return_value = (100, None)

    monitor_job()

    mock_check_endpoint.assert_called_with('http://example.com')
    mock_check_ssl.assert_called_with('http://example.com')
    mock_add_result.assert_called_once()
    mock_send_alert.assert_not_called()

@patch('main.check_endpoint')
@patch('main.check_ssl_expiry')
@patch('main.add_result')
@patch('main.analyze_failure')
@patch('main.send_alert')
@patch('main.MONITOR_ENDPOINTS', ['http://example.com'])
def test_monitor_job_down(mock_send_alert, mock_analyze, mock_add_result, mock_check_ssl, mock_check_endpoint):
    mock_check_endpoint.return_value = (500, 0.1, "Internal Server Error")
    mock_check_ssl.return_value = (100, None)
    mock_analyze.return_value = "Diagnosis"

    monitor_job()

    mock_analyze.assert_called_with('http://example.com', 500, 0.1, "Internal Server Error")
    mock_send_alert.assert_called_with('http://example.com', "Internal Server Error", "Diagnosis")
    mock_add_result.assert_called_once()

@patch('main.check_endpoint')
@patch('main.check_ssl_expiry')
@patch('main.add_result')
@patch('main.analyze_failure')
@patch('main.send_alert')
@patch('main.MONITOR_ENDPOINTS', ['http://example.com'])
def test_monitor_job_ssl_warning_and_errors(mock_send_alert, mock_analyze, mock_add_result, mock_check_ssl, mock_check_endpoint):
    mock_analyze.return_value = "Mocked Analysis"

    # Test SSL error combination with HTTP error
    mock_check_endpoint.return_value = (500, 0.1, "HTTP Error")
    mock_check_ssl.return_value = (None, "SSL Err")
    monitor_job()
    
    # Test SSL error without HTTP error
    mock_check_endpoint.return_value = (200, 0.1, None)
    mock_check_ssl.return_value = (None, "SSL Cert Invalid")
    monitor_job()

    # Test SSL expiration warning
    mock_check_endpoint.return_value = (200, 0.1, None)
    mock_check_ssl.return_value = (10, None)
    monitor_job()
    assert mock_send_alert.called

@patch('main.MONITOR_ENDPOINTS', [])
@patch('main.check_endpoint')
def test_monitor_job_empty(mock_check_endpoint):
    monitor_job()
    mock_check_endpoint.assert_not_called()

@patch('main.BlockingScheduler')
@patch('main.monitor_job')
def test_main_func(mock_monitor_job, mock_scheduler):
    instance = mock_scheduler.return_value
    main()
    instance.add_job.assert_called()
    instance.start.assert_called()
    mock_monitor_job.assert_called()

    # Test exception
    instance.start.side_effect = KeyboardInterrupt
    main()

from apscheduler.schedulers.blocking import BlockingScheduler

@patch.object(BlockingScheduler, 'start')
def test_main_block(mock_start):
    import runpy
    import os
    runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "main.py"), run_name="__main__")
    mock_start.assert_called()
