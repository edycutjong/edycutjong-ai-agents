import pytest
import pandas as pd
from agent.kpi_engine import KPIEngine, KPIDefinition

def test_calculate_metric_sum():
    df = pd.DataFrame({'sales': [10, 20, 30]})
    kpi = KPIDefinition("Total Sales", "sales", "sum", 100)
    val = KPIEngine.calculate_metric(df, kpi)
    assert val == 60

def test_calculate_metric_avg():
    df = pd.DataFrame({'sales': [10, 20, 30]})
    kpi = KPIDefinition("Avg Sales", "sales", "avg", 20)
    val = KPIEngine.calculate_metric(df, kpi)
    assert val == 20

def test_calculate_metric_count():
    df = pd.DataFrame({'sales': [10, 20, 30]})
    kpi = KPIDefinition("Count", "sales", "count", 3)
    val = KPIEngine.calculate_metric(df, kpi)
    assert val == 3

def test_calculate_metric_rows():
    df = pd.DataFrame({'sales': [10, 20, 30]})
    kpi = KPIDefinition("Rows", "Rows", "count", 3)
    val = KPIEngine.calculate_metric(df, kpi)
    assert val == 3

def test_evaluate_status_higher_is_better():
    assert KPIEngine.evaluate_status(100, 100) == "success"
    assert KPIEngine.evaluate_status(90, 100) == "warning"
    assert KPIEngine.evaluate_status(80, 100) == "danger"

def test_evaluate_status_lower_is_better():
    assert KPIEngine.evaluate_status(100, 100, logic='lower_is_better') == "success"
    assert KPIEngine.evaluate_status(110, 100, logic='lower_is_better') == "warning"
    assert KPIEngine.evaluate_status(120, 100, logic='lower_is_better') == "danger"
