import pytest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import requests
import socket

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.monitor import check_endpoint, check_ssl_expiry, check_custom_regex

# Helper for patching socket in all tests
@pytest.fixture(autouse=True)
def mock_dns():
    with patch('agent.monitor.socket.getaddrinfo') as mock:
        # Default to a safe IP (IPv4)
        mock.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('93.184.216.34', 80))]
        yield mock

@patch('agent.monitor.requests.request')
def test_check_endpoint(mock_request):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.is_redirect = False
    mock_request.return_value = mock_response

    status_code, response_time, error = check_endpoint("https://example.com")
    assert status_code == 200
    assert response_time >= 0
    assert error is None

@patch('agent.monitor.requests.request')
def test_check_endpoint_error(mock_request):
    # Use RequestException so it gets caught
    mock_request.side_effect = requests.exceptions.RequestException("Connection refused")

    status_code, response_time, error = check_endpoint("https://example.com")
    assert status_code == 0
    assert error == "Connection refused"

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
    mock_cert = {'notAfter': future_date.strftime('%b %d %H:%M:%S %Y GMT')}
    mock_ssock.getpeercert.return_value = mock_cert

    days_to_expiry, error = check_ssl_expiry("https://example.com")
    assert days_to_expiry > 300
    assert error is None

@patch('agent.monitor.requests.request')
def test_check_custom_regex(mock_request):
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

# New Security Tests

def test_ssrf_check_endpoint_private_ip():
    with patch('agent.monitor.socket.getaddrinfo') as mock_dns:
        mock_dns.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 80))]
        status, _, error = check_endpoint("http://localhost")
        assert status == 0
        assert "Access to local/private resource" in error

def test_ssrf_check_endpoint_invalid_scheme():
    status, _, error = check_endpoint("ftp://example.com")
    assert status == 0
    assert "Invalid scheme" in error

def test_ssrf_check_ssl_expiry_private_ip():
    with patch('agent.monitor.socket.getaddrinfo') as mock_dns:
        mock_dns.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('10.0.0.1', 443))]
        days, error = check_ssl_expiry("https://internal.service")
        assert days is None
        assert "Access to local/private resource" in error

def test_ssrf_check_custom_regex_private_ip():
    with patch('agent.monitor.socket.getaddrinfo') as mock_dns:
        mock_dns.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('169.254.169.254', 80))]
        match, error = check_custom_regex("http://metadata", "secret")
        assert match is False
        assert "Access to local/private resource" in error

def test_ssrf_redirect_to_private_ip():
    # Mock requests.request to return a redirect first, then verify the second call
    with patch('agent.monitor.requests.request') as mock_request:

        def side_effect_dns(host, *args, **kwargs):
            if host == 'example.com':
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('93.184.216.34', 80))]
            elif host == 'localhost':
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 80))]
            return []

        with patch('agent.monitor.socket.getaddrinfo', side_effect=side_effect_dns):
            # First response is a redirect
            resp1 = Mock()
            resp1.status_code = 302
            resp1.is_redirect = True
            resp1.headers = {'Location': 'http://localhost/admin'}

            mock_request.side_effect = [resp1]

            status, _, error = check_endpoint("http://example.com")

            assert status == 0
            assert "Access to local/private resource 127.0.0.1 is denied" in error
            assert mock_request.call_count == 1

def test_ssrf_ipv6_loopback():
    with patch('agent.monitor.socket.getaddrinfo') as mock_dns:
        # IPv6 loopback ::1
        mock_dns.return_value = [(socket.AF_INET6, socket.SOCK_STREAM, 6, '', ('::1', 80, 0, 0))]
        status, _, error = check_endpoint("http://[::1]")
        assert status == 0
        assert "Access to local/private resource" in error
