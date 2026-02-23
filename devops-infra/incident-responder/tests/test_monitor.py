import pytest
from agent.monitor import LogMonitor

def test_monitor_initialization():
    monitor = LogMonitor()
    assert monitor.services
    assert monitor.error_types
    assert monitor.log_levels

def test_generate_log_entry():
    monitor = LogMonitor()
    log_entry = monitor.generate_log_entry()
    assert "timestamp" in log_entry
    assert "service" in log_entry
    assert "level" in log_entry
    assert "message" in log_entry

def test_get_log_batch():
    monitor = LogMonitor()
    batch = monitor.get_log_batch(count=5)
    assert len(batch) == 5
    for log in batch:
        assert isinstance(log, dict)
