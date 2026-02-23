import pytest
import pandas as pd
import os

@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Sales': [100, 150, 120],
        'Region': ['North', 'South', 'North']
    })
    path = tmp_path / "test_data.csv"
    df.to_csv(path, index=False)
    return str(path)

@pytest.fixture
def sample_json(tmp_path):
    df = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Sales': [100, 150, 120],
        'Region': ['North', 'South', 'North']
    })
    path = tmp_path / "test_data.json"
    df.to_json(path, orient='records')
    return str(path)

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Sales': [100, 150, 120],
        'Region': ['North', 'South', 'North']
    })
