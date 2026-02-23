import os
import pytest
from agent.python_plotter import generate_python_chart
from agent.js_generator import generate_js_chart

def test_generate_python_chart(sample_df, tmp_path):
    output_path = tmp_path / "chart.png"
    result = generate_python_chart(sample_df, 'bar', 'Date', 'Sales', 'Test Chart', str(output_path))
    assert os.path.exists(result)
    assert result == str(output_path)

def test_generate_python_chart_error(sample_df):
    with pytest.raises(ValueError):
        generate_python_chart(sample_df, 'invalid_type', 'Date', 'Sales')

def test_generate_js_chart(sample_df, tmp_path):
    output_path = tmp_path / "chart.html"
    result = generate_js_chart(sample_df, 'line', 'Date', 'Sales', 'Test JS Chart', str(output_path))
    assert os.path.exists(result)
    assert result == str(output_path)
    with open(result, 'r') as f:
        content = f.read()
        assert "Test JS Chart" in content
        assert "chart.js" in content
