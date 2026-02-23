import pytest
import pandas as pd
from agent.data_loader import load_data

def test_load_csv(sample_csv):
    df = load_data(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert 'Sales' in df.columns

def test_load_json(sample_json):
    df = load_data(sample_json)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert 'Region' in df.columns

def test_invalid_format():
    with pytest.raises(ValueError):
        load_data("test.txt")
