import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def source_df():
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'score': [80.5, 90.0, 85.5, 88.0, 92.5]
    }
    return pd.DataFrame(data)

@pytest.fixture
def dest_df():
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'score': [80.5, 90.0, 85.5, 88.0, 92.5]
    }
    return pd.DataFrame(data)

@pytest.fixture
def dest_df_mismatch():
    data = {
        'id': [1, 2, 3, 4], # Missing one row
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40],
        'score': [80.5, 90.0, 85.5, 88.0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def dest_df_schema_change():
    data = {
        'user_id': [1, 2, 3, 4, 5], # Renamed column
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'score': [80, 90, 85, 88, 92] # Int instead of float
    }
    return pd.DataFrame(data)
