import pytest
import pandas as pd
from io import StringIO
import sys
import os

# Add parent dir to sys.path to import agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.analyzer import Analyzer

def test_infer_schema():
    csv_data = """name,age,score,is_active
Alice,30,85.5,True
Bob,25,90.0,False"""

    file = StringIO(csv_data)
    analyzer = Analyzer(file)
    schema = analyzer.infer_schema()

    assert len(schema) == 4

    schema_dict = {col['original_name']: col['type'] for col in schema}
    assert schema_dict['name'] == 'str'
    assert schema_dict['age'] == 'int'
    assert schema_dict['score'] == 'float'
    assert schema_dict['is_active'] == 'bool'

def test_infer_schema_datetime():
    csv_data = """event,date
Launch,2023-01-01
End,2023-12-31"""

    file = StringIO(csv_data)
    analyzer = Analyzer(file)
    schema = analyzer.infer_schema()

    schema_dict = {col['original_name']: col['type'] for col in schema}
    # Should infer datetime if format is clear
    assert schema_dict['date'] == 'datetime'
