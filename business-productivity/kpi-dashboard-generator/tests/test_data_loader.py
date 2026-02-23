import pytest
import pandas as pd
import io
from unittest.mock import patch, Mock
from agent.data_loader import DataLoader

def test_load_csv():
    csv_content = "col1,col2\n1,2\n3,4"
    buffer = io.BytesIO(csv_content.encode('utf-8'))
    df = DataLoader.load_csv(buffer)
    assert len(df) == 2
    assert 'col1' in df.columns

def test_load_api_json_list():
    mock_response = Mock()
    mock_response.json.return_value = [{"col1": 1, "col2": 2}, {"col1": 3, "col2": 4}]
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response):
        df = DataLoader.load_api_json("http://fake.url")
        assert len(df) == 2
        assert 'col1' in df.columns

def test_load_api_json_dict_with_list():
    mock_response = Mock()
    mock_response.json.return_value = {"data": [{"col1": 1}, {"col1": 2}]}
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response):
        df = DataLoader.load_api_json("http://fake.url")
        assert len(df) == 2

def test_load_api_error():
    with patch('requests.get', side_effect=Exception("Connection Error")):
        with pytest.raises(ValueError):
            DataLoader.load_api_json("http://fake.url")
