import pytest
from click.testing import CliRunner
import json
from unittest.mock import patch, AsyncMock, MagicMock
from main import main, run_probes
from lib.budget import BudgetManager
from lib.log_parser import parse_access_logs
from lib.alerter import send_alert
import lib.prober as prober

def test_budget_manager_empty():
    bm = BudgetManager({})
    res = bm.evaluate([], {"p50": 100}, 1.0)
    assert res["total_requests"] == 0

def test_budget_manager_no_slo_target():
    bm = BudgetManager({})
    res = bm.evaluate([10, 20], {}, 1.0)
    assert res["total_requests"] == 2
    assert res["violations"] == 0

def test_budget_manager_p50_target():
    bm = BudgetManager({})
    res = bm.evaluate([100, 200, 300], {"p50": 150}, 10.0)
    assert res["total_requests"] == 3
    assert res["violations"] == 2 

def test_budget_manager_p95_target():
    bm = BudgetManager({})
    res = bm.evaluate([100, 200, 300], {"p95": 250}, 10.0)
    assert res["total_requests"] == 3
    assert res["violations"] == 1 

def test_budget_manager_exhausted():
    bm = BudgetManager({})
    res = bm.evaluate([1000, 1000, 1000, 1000, 1000], {"p99": 500}, 1.0)
    assert res["is_exhausted"] == True

def test_log_parser():
    logs = [
        '{"path": "/users", "latency_ms": "100", "status": "200"}',
        '{"path": "/users", "latency_ms": 1200, "status": 500}',
        '{"path": "/different", "latency_ms": 50}',
        'not a json',
        '{}'
    ]
    res = parse_access_logs(logs, endpoint_path="users")
    assert len(res) == 2
    assert res[0] == 100.0
    assert res[1] == float('inf')

def test_log_parser_no_path_filter():
    logs = ['{"path": "/users", "latency_ms": 100}']
    res = parse_access_logs(logs)
    assert len(res) == 1
    assert res[0] == 100.0

@pytest.mark.asyncio
async def test_prober_success(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    
    # We mock AsyncClient's async context manager
    # httpx.AsyncClient().__aenter__ is an AsyncMock that returns mock_client_instance
    mock_client_instance = mocker.AsyncMock()
    mock_client_instance.request.return_value = mock_response

    mock_client_class_instance = mocker.MagicMock()
    mock_client_class_instance.__aenter__.return_value = mock_client_instance
    
    mocker.patch("httpx.AsyncClient", return_value=mock_client_class_instance)
    
    success, latency = await prober.probe_endpoint({"url": "http://test", "method": "GET"})
    assert success is True
    assert latency >= 0

@pytest.mark.asyncio
async def test_prober_failure(mocker):
    mock_client_class_instance = mocker.MagicMock()
    mock_client_class_instance.__aenter__.side_effect = Exception("failed")
    mocker.patch("httpx.AsyncClient", return_value=mock_client_class_instance)
    
    success, latency = await prober.probe_endpoint({"url": "http://test"})
    assert success is False
    assert latency == float('inf')

@pytest.mark.asyncio
async def test_run_probes_func(mocker):
    # Mock probe_endpoint which is called by run_probes
    mocker.patch("main.probe_endpoint", return_value=(True, 150.0))
    res = await run_probes([{"name": "test", "url": "http"}], iterations=2)
    assert len(res["test"]) == 2

def test_alerter_success(mocker):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mocker.patch("httpx.post", return_value=mock_resp)
    assert send_alert("http://hook", "msg") is True

def test_alerter_no_url():
    assert send_alert("", "msg") is False

def test_alerter_exception(mocker):
    mocker.patch("httpx.post", side_effect=Exception("error"))
    assert send_alert("http://hook", "msg") is False

def test_cli_missing_config():
    runner = CliRunner()
    result = runner.invoke(main, ["--config", "missing.yaml"])
    assert result.exit_code == 1

def test_cli_missing_logs(mock_config_yml):
    runner = CliRunner()
    result = runner.invoke(main, ["--config", mock_config_yml, "--logs", "missing.txt"])
    assert result.exit_code == 1

def test_cli_with_logs_table(mock_config_yml, mock_logs_json):
    runner = CliRunner()
    result = runner.invoke(main, ["--config", mock_config_yml, "--logs", mock_logs_json, "--format", "table"])
    assert result.exit_code == 1
    assert "EXHAUSTED" in result.output

@patch("main.send_alert")
def test_cli_with_logs_json(mock_alert, mock_config_yml, mock_logs_json):
    runner = CliRunner()
    result = runner.invoke(main, ["--config", mock_config_yml, "--logs", mock_logs_json, "--format", "json"])
    assert result.exit_code == 1
    assert mock_alert.called

def test_cli_with_logs_md_warn_only(empty_config_yml, mock_logs_json):
    runner = CliRunner()
    result = runner.invoke(main, ["--config", empty_config_yml, "--logs", mock_logs_json, "--format", "markdown"])
    assert result.exit_code == 0
    assert "OK" in result.output

@patch("main.run_probes")
def test_cli_with_synthetic_probes(mock_run_probes, empty_config_yml):
    # Return mock async result
    mock_run_probes.return_value = {"Empty API": [100.0, 200.0]}
    runner = CliRunner()
    result = runner.invoke(main, ["--config", empty_config_yml, "--format", "table"])
    assert result.exit_code == 0
    assert "OK" in result.output
    
def test_cli_root_url(root_url_config_yml, mock_logs_json):
    runner = CliRunner()
    result = runner.invoke(main, ["--config", root_url_config_yml, "--logs", mock_logs_json, "--format", "table"])
    assert result.exit_code == 0

@patch("main.run_probes")
def test_cli_with_synthetic_probes_warning(mock_run_probes, mock_config_warn_yml):
    mock_run_probes.return_value = {"Warn API": [1200.0, 100.0, 100.0]}
    # 3 total requests, budget = 100% -> allowable = 3
    # violations = 1
    # 1/3 * 100 = 33% consumed -> NOT exhausted, NOT warning (>80%) - let's make it 90%
    # If 9 requests, 3 violate, budget = 33.3%, allowable 3. 3/3 = 100%. 
    # Just need 10 requests, 9 violate, budget 100% -> allowable 10. violations 9. consumed 90%.
    mock_run_probes.return_value = {"Warn API": [1200.0] * 9 + [100.0]}
    
    runner = CliRunner()
    result = runner.invoke(main, ["--config", mock_config_warn_yml, "--format", "table"])
    assert result.exit_code == 0
    assert "WARNING" in result.output
