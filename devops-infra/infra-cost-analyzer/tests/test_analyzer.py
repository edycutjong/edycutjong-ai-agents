import pytest
import pandas as pd
from datetime import datetime, timedelta
from agent.analyzer import CostAnalyzer

@pytest.fixture
def sample_data():
    data = {
        'Service': ['EC2', 'EC2', 'S3', 'ElasticIP'],
        'ResourceID': ['i-1', 'i-2', 'bucket-1', 'eip-1'],
        'Cost': [10.0, 5.0, 2.0, 0.5],
        'Date': [
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        ],
        'CPUUtilization': [50.0, 2.0, None, None]
    }
    return pd.DataFrame(data)

def test_calculate_total_cost(sample_data):
    analyzer = CostAnalyzer(sample_data)
    total = analyzer.calculate_total_cost()
    assert total == 17.5

def test_identify_waste(sample_data):
    analyzer = CostAnalyzer(sample_data)
    waste = analyzer.identify_potential_waste()

    # Expect i-2 (low CPU) and eip-1 (ElasticIP with cost) to be flagged
    assert not waste.empty
    reasons = waste['Reason'].tolist()
    assert any("Low CPU" in r for r in reasons)
    assert any("Potential Unattached IP" in r for r in reasons)

def test_detect_anomalies():
    # Create spike data
    dates = pd.date_range(start='2023-01-01', periods=10)
    costs = [10.0] * 9 + [100.0] # Spike on last day
    data = pd.DataFrame({'Date': dates, 'Cost': costs, 'Service': 'Test'})

    analyzer = CostAnalyzer(data)
    anomalies = analyzer.detect_anomalies()

    assert not anomalies.empty
    assert anomalies.iloc[0]['Cost'] == 100.0
