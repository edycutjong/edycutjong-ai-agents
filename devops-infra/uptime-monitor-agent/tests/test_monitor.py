import pytest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import requests

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.monitor import check_endpoint, check_ssl_expiry, check_custom_regex

@patch('agent.monitor.requests.Session.request')
@patch('agent.monitor.socket.getaddrinfo')
def test_check_endpoint(mock_getaddrinfo, mock_request):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('8.8.8.8', 80))]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.is_redirect = False
    mock_request.return_value = mock_response

    status_code, response_time, error = check_endpoint("https://example.com")
    assert status_code == 200
    assert response_time >= 0
    assert error is None

@patch('agent.monitor.requests.Session.request')
@patch('agent.monitor.socket.getaddrinfo')
def test_check_endpoint_error(mock_getaddrinfo, mock_request):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('8.8.8.8', 80))]

    # Use RequestException so it gets caught
    mock_request.side_effect = requests.exceptions.RequestException("Connection refused")

    status_code, response_time, error = check_endpoint("https://example.com")
    assert status_code == 0
    assert "Connection refused" in error

@patch('agent.monitor.ssl.create_default_context')
@patch('agent.monitor.socket.create_connection')
def test_check_ssl_expiry(mock_create_connection, mock_create_context):
    mock_socket = Mock()
    mock_create_connection.return_value.__enter__.return_value = mock_socket

    mock_ssock = Mock()
    # Use MagicMock for context to support context manager
    mock_context = MagicMock()
    mock_create_context.return_value = mock_context
    mock_context.wrap_socket.return_value.__enter__.return_value = mock_ssock

    # Mock certificate
    future_date = datetime.utcnow().replace(year=datetime.utcnow().year + 1)
    # Ensure format matches exactly what strptime expects
    # %b %d %H:%M:%S %Y %Z
    mock_cert = {'notAfter': future_date.strftime('%b %d %H:%M:%S %Y GMT')}
    mock_ssock.getpeercert.return_value = mock_cert

    days_to_expiry, error = check_ssl_expiry("https://example.com")
    assert days_to_expiry > 300
    assert error is None

@patch('agent.monitor.requests.Session.request')
@patch('agent.monitor.socket.getaddrinfo')
def test_check_custom_regex(mock_getaddrinfo, mock_request):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('8.8.8.8', 80))]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.is_redirect = False
    mock_response.text = "Hello World"
    mock_request.return_value = mock_response

    match, error = check_custom_regex("https://example.com", "World")
    assert match is True
    assert error is None

    match, error = check_custom_regex("https://example.com", "Foo")
    assert match is False
    assert "not found" in error

@patch('agent.monitor.socket.getaddrinfo')
def test_ssrf_blocked_localhost(mock_getaddrinfo):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('127.0.0.1', 80))]

    status_code, response_time, error = check_endpoint("http://localhost:8080")
    assert status_code == 0
    assert "SSRF Validation Failed" in error

@patch('agent.monitor.socket.getaddrinfo')
def test_ssrf_blocked_internal(mock_getaddrinfo):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('10.0.0.1', 80))]

    status_code, response_time, error = check_endpoint("http://internal.company.com")
    assert status_code == 0
    assert "SSRF Validation Failed" in error
    assert "Unsafe IP" in error

@patch('agent.monitor.requests.Session.request')
@patch('agent.monitor.socket.getaddrinfo')
def test_ssrf_blocked_redirect(mock_getaddrinfo, mock_request):
    # First resolve is external, second resolve (redirect) is internal
    mock_getaddrinfo.side_effect = [
        [(2, 1, 6, '', ('8.8.8.8', 80))],
        [(2, 1, 6, '', ('169.254.169.254', 80))]
    ]

    mock_response = Mock()
    mock_response.is_redirect = True
    mock_response.headers = {'Location': 'http://169.254.169.254/latest/meta-data'}
    mock_request.return_value = mock_response

    status_code, response_time, error = check_endpoint("http://external.com")
    assert status_code == 0
    assert "SSRF Validation Failed" in error
    assert "Unsafe IP" in error

@patch('agent.monitor.socket.getaddrinfo')
def test_ssrf_blocked_ssl_expiry(mock_getaddrinfo):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('127.0.0.1', 80))]

    days_to_expiry, error = check_ssl_expiry("https://localhost:8443")
    assert days_to_expiry is None
    assert "SSRF Validation Failed" in error

@patch('agent.monitor.socket.getaddrinfo')
def test_ssrf_blocked_custom_regex(mock_getaddrinfo):
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('127.0.0.1', 80))]

    match, error = check_custom_regex("http://localhost:8080", "pattern")
    assert match is False
    assert "SSRF Validation Failed" in error
