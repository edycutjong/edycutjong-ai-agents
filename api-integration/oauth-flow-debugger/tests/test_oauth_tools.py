import pytest
import jwt
import sys
import os
from unittest.mock import MagicMock

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import oauth_tools

def test_generate_auth_url():
    url = oauth_tools.generate_auth_url(
        client_id="123",
        auth_url="https://example.com/auth",
        redirect_uri="https://app.com/callback",
        scopes="read write",
        state="xyz"
    )
    assert "client_id=123" in url
    assert "redirect_uri=https%3A%2F%2Fapp.com%2Fcallback" in url
    assert "scope=read+write" in url
    assert "state=xyz" in url
    assert "response_type=code" in url

def test_exchange_code_for_token(mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "token123"}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = oauth_tools.exchange_code_for_token(
        "id", "secret", "https://token.url", "code123", "https://cb"
    )
    assert result == {"access_token": "token123"}
    mock_post.assert_called_once()

def test_get_client_credentials_token(mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "cc_token"}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = oauth_tools.get_client_credentials_token(
        "id", "secret", "https://token.url", "read"
    )
    assert result == {"access_token": "cc_token"}

def test_refresh_access_token(mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "new_token"}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = oauth_tools.refresh_access_token(
        "id", "secret", "https://token.url", "refresh_123"
    )
    assert result == {"access_token": "new_token"}

def test_validate_redirect_uri():
    assert oauth_tools.validate_redirect_uri("https://localhost/cb") == []
    # http://example.com is invalid (should be https)
    issues = oauth_tools.validate_redirect_uri("http://example.com")
    assert any("HTTPS" in issue for issue in issues)

    # Fragment check
    issues_fragment = oauth_tools.validate_redirect_uri("https://example.com#fragment")
    assert any("fragment" in issue for issue in issues_fragment)

def test_decode_jwt():
    # Create a dummy token
    payload = {"sub": "123", "name": "Test"}
    token = jwt.encode(payload, "secret", algorithm="HS256")

    result = oauth_tools.decode_jwt(token)
    assert result["valid_structure"] is True
    assert result["payload"]["sub"] == "123"

    result_invalid = oauth_tools.decode_jwt("invalid.token")
    assert result_invalid["valid_structure"] is False
