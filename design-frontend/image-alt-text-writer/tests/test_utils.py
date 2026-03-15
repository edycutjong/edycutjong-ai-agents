import pytest
import os
import base64
from unittest.mock import patch, mock_open, MagicMock
import requests
from agent.utils import encode_image, get_image_data

def test_encode_image_success():
    m = mock_open(read_data=b"testdata")
    with patch('builtins.open', m):
        encoded = encode_image("test.jpg")
        assert encoded == base64.b64encode(b"testdata").decode('utf-8')

def test_encode_image_exception():
    with patch('builtins.open', side_effect=Exception("mocked error")):
        with patch('builtins.print') as mock_print:
            encoded = encode_image("test.jpg")
            assert encoded is None
            mock_print.assert_called_once()

@patch('requests.get')
def test_get_image_data_url_success(mock_get):
    mock_response = MagicMock()
    mock_response.content = b"testdata"
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    encoded = get_image_data("http://example.com/image.jpg")
    assert encoded == base64.b64encode(b"testdata").decode('utf-8')
    mock_get.assert_called_once_with("http://example.com/image.jpg", timeout=10)

@patch('requests.get')
def test_get_image_data_url_exception(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("mocked error")
    with patch('builtins.print') as mock_print:
        encoded = get_image_data("http://example.com/image.jpg")
        assert encoded is None
        mock_print.assert_called_once()

@patch('os.path.exists', return_value=True)
def test_get_image_data_local_no_base_path(mock_exists):
    m = mock_open(read_data=b"testdata")
    with patch('builtins.open', m):
        encoded = get_image_data("test.jpg")
        assert encoded == base64.b64encode(b"testdata").decode('utf-8')

@patch('os.path.exists', return_value=False)
def test_get_image_data_local_not_found(mock_exists):
    with patch('builtins.print') as mock_print:
        encoded = get_image_data("test.jpg", base_path="/some/path")
        assert encoded is None
        mock_print.assert_called_once()
