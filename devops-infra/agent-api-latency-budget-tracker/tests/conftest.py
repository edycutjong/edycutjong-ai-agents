import pytest
import os

@pytest.fixture
def mock_config_yml(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
endpoints:
  - name: "Test API"
    url: "https://example.com/api"
    slo:
      p99: 1000
budget:
  total_error_budget_percentage: 1.0
alerting:
  webhook_url: "https://hooks.slack.com/test"
""")
    return str(config_file)

@pytest.fixture
def mock_config_warn_yml(tmp_path):
    config_file = tmp_path / "config_warn.yaml"
    config_file.write_text("""
endpoints:
  - name: "Warn API"
    url: "https://example.com/api"
    slo:
      p99: 1000
budget:
  total_error_budget_percentage: 100.0
""")
    return str(config_file)

@pytest.fixture
def root_url_config_yml(tmp_path):
    config_file = tmp_path / "root_config.yaml"
    config_file.write_text("""
endpoints:
  - name: "Root API"
    url: "https://example.com/"
    slo: {}
""")
    return str(config_file)

@pytest.fixture
def empty_config_yml(tmp_path):
    config_file = tmp_path / "empty_config.yaml"
    config_file.write_text("""
endpoints:
  - name: "Empty API"
    url: "/empty"
    slo: {}
""")
    return str(config_file)


@pytest.fixture
def mock_logs_json(tmp_path):
    logs_file = tmp_path / "access.log"
    logs_file.write_text("""
{"path": "/api", "latency_ms": 150.0, "status": 200}
{"path": "/api", "latency_ms": 1200.0, "status": 200}
{"path": "/api", "latency_ms": 5000.0, "status": 500}
invalid json string
{"path": "/wrong", "latency_ms": 50.0, "status": 200}
""")
    return str(logs_file)
