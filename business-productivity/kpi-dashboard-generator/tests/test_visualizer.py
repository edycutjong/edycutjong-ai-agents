import pytest
import pandas as pd
from agent.visualizer import Visualizer

def test_create_trend_chart():
    df = pd.DataFrame({
        'date': pd.date_range('2023-01-01', periods=5),
        'value': [1, 2, 3, 4, 5]
    })
    fig = Visualizer.create_trend_chart(df, 'date', 'value')
    assert fig is not None
    # Check if it's a plotly figure
    assert hasattr(fig, 'to_json')

def test_create_bar_chart():
    df = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B'],
        'value': [10, 20, 30, 40]
    })
    fig = Visualizer.create_bar_chart(df, 'category', 'value', aggregation='sum')
    assert fig is not None
    assert hasattr(fig, 'to_json')
