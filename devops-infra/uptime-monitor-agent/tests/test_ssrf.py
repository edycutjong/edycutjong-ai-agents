import pytest
from unittest.mock import patch
import requests

from agent.monitor import check_endpoint, check_custom_regex

@patch('socket.getaddrinfo')
def test_ssrf_blocked(mock_getaddrinfo):
    # Mocking internal IP resolution
    mock_getaddrinfo.return_value = [
        (2, 1, 6, '', ('127.0.0.1', 80))
    ]

    status, time, err = check_endpoint("http://internal-service.local")
    assert status == 0
    assert "Unsafe IP" in err or "SSRF" in err or "Invalid" in err
