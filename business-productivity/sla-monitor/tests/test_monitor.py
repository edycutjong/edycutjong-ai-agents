"""Tests for SLA Monitor."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.monitor import SLADefinition, SLAMeasurement, SLAStatus, check_compliance, calculate_uptime, calculate_compliance_rate, get_breach_report, format_sla_dashboard

UPTIME_SLA = SLADefinition(name="API Uptime", metric="uptime", target=99.9, unit="%", warning_threshold=0.1)
RESPONSE_SLA = SLADefinition(name="Response Time", metric="response_time", target=200, unit="ms", warning_threshold=50)
ERROR_SLA = SLADefinition(name="Error Rate", metric="error_rate", target=1.0, unit="%")

def test_uptime_compliant():
    s = check_compliance(UPTIME_SLA, 99.95)
    assert s.is_compliant

def test_uptime_breach():
    s = check_compliance(UPTIME_SLA, 99.5)
    assert not s.is_compliant

def test_uptime_warning():
    s = check_compliance(UPTIME_SLA, 99.95)
    assert s.is_warning  # within warning threshold

def test_response_compliant():
    s = check_compliance(RESPONSE_SLA, 150)
    assert s.is_compliant

def test_response_breach():
    s = check_compliance(RESPONSE_SLA, 350)
    assert not s.is_compliant

def test_error_compliant():
    s = check_compliance(ERROR_SLA, 0.5)
    assert s.is_compliant

def test_error_breach():
    s = check_compliance(ERROR_SLA, 2.5)
    assert not s.is_compliant

def test_margin_uptime():
    s = check_compliance(UPTIME_SLA, 99.95)
    assert s.margin == pytest.approx(0.05, abs=0.01)

def test_margin_response():
    s = check_compliance(RESPONSE_SLA, 150)
    assert s.margin == 50

def test_calculate_uptime():
    assert calculate_uptime(43200, 43.2) == pytest.approx(99.9, abs=0.01)

def test_calculate_uptime_zero():
    assert calculate_uptime(0, 0) == 0

def test_compliance_rate():
    statuses = [SLAStatus(sla=UPTIME_SLA, is_compliant=True), SLAStatus(sla=RESPONSE_SLA, is_compliant=False)]
    assert calculate_compliance_rate(statuses) == 50.0

def test_compliance_all():
    statuses = [SLAStatus(sla=UPTIME_SLA, is_compliant=True)]
    assert calculate_compliance_rate(statuses) == 100.0

def test_breach_report():
    statuses = [SLAStatus(sla=UPTIME_SLA, is_compliant=True, current_value=99.99), SLAStatus(sla=RESPONSE_SLA, is_compliant=False, current_value=300)]
    breaches = get_breach_report(statuses)
    assert len(breaches) == 1
    assert breaches[0]["name"] == "Response Time"

def test_format_dashboard():
    statuses = [check_compliance(UPTIME_SLA, 99.95), check_compliance(RESPONSE_SLA, 150)]
    md = format_sla_dashboard(statuses)
    assert "SLA Dashboard" in md
    assert "API Uptime" in md

def test_to_dict():
    s = check_compliance(UPTIME_SLA, 99.95)
    d = s.to_dict()
    assert "name" in d and "compliant" in d

def test_measurement():
    m = SLAMeasurement(sla_name="API", value=99.99)
    assert m.timestamp
    assert m.to_dict()["value"] == 99.99
