import pytest
import json
from agent.metrics import MetricExtractor
from agent.prometheus import PrometheusGenerator
from agent.grafana import GrafanaGenerator
from agent.documentation import DocGenerator

MOCK_LOGS = [
    {"timestamp": "2023-10-27T10:00:00Z", "level": "INFO", "service": "test", "message": "msg", "metadata": {"duration": 0.1}}
]

MOCK_METRICS = [
    {
        "name": "test_metric",
        "type": "COUNTER",
        "description": "Test metric",
        "labels": ["service"],
        "source_field": "level",
        "unit": "count"
    }
]

def test_metric_extractor_mock():
    extractor = MetricExtractor(api_key=None)
    metrics = extractor.extract(MOCK_LOGS)
    assert len(metrics) > 0
    assert "name" in metrics[0]

def test_prometheus_generator_mock():
    gen = PrometheusGenerator(api_key=None)
    config = gen.generate(MOCK_METRICS)
    assert "scrape_configs" in config
    assert "test_metric" in config

def test_grafana_generator_mock():
    gen = GrafanaGenerator(api_key=None)
    dashboard_json = gen.generate(MOCK_METRICS, "test-service")
    dashboard = json.loads(dashboard_json)
    # Mock may return {"title": ...} or nested {"dashboard": {"title": ...}}
    if "dashboard" in dashboard:
        assert "Dashboard" in dashboard["dashboard"]["title"]
    else:
        assert "Dashboard" in dashboard["title"]

def test_doc_generator_mock():
    gen = DocGenerator(api_key=None)
    docs = gen.generate(MOCK_METRICS)
    assert "Metric" in docs
    assert "test_metric" in docs

def test_empty_inputs():
    assert MetricExtractor(api_key=None).extract([]) == []
    assert PrometheusGenerator(api_key=None).generate([]) == ""
    assert GrafanaGenerator(api_key=None).generate([], "svc") == ""
    assert DocGenerator(api_key=None).generate([]) == ""
