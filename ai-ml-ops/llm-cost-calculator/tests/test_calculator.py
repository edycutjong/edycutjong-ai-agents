"""Tests for calculator module."""
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.calculator import (
    UsageEntry, calculate_cost, generate_cost_report,
    forecast_monthly_cost, check_budget, format_report_markdown,
)


def test_calculate_cost_known_model():
    """Calculates cost correctly for gpt-4o."""
    result = calculate_cost("gpt-4o", 1_000_000, 1_000_000)
    assert result["input_cost"] == 2.50
    assert result["output_cost"] == 10.00
    assert result["total_cost"] == 12.50
    assert result["provider"] == "OpenAI"


def test_calculate_cost_small_tokens():
    """Calculates cost for small token counts."""
    result = calculate_cost("gpt-4o-mini", 100, 50)
    assert result["total_cost"] > 0
    assert result["total_cost"] < 0.001  # very cheap


def test_calculate_cost_unknown_model():
    """Returns error for unknown model."""
    result = calculate_cost("nonexistent", 1000, 500)
    assert "error" in result
    assert result["total_cost"] == 0.0


def test_usage_entry_roundtrip():
    """UsageEntry serializes and deserializes correctly."""
    entry = UsageEntry(model="gpt-4o", input_tokens=1000, output_tokens=500,
                       timestamp="2026-01-01T00:00:00", label="test")
    d = entry.to_dict()
    restored = UsageEntry.from_dict(d)
    assert restored.model == "gpt-4o"
    assert restored.input_tokens == 1000
    assert restored.label == "test"


def test_generate_cost_report(sample_entries):
    """Report has all expected keys and correct totals."""
    report = generate_cost_report(sample_entries)
    assert report["total_calls"] == 5
    assert report["total_cost"] > 0
    assert "by_model" in report
    assert "by_provider" in report
    assert "by_label" in report
    assert "high_cost_queries" in report
    assert len(report["by_model"]) >= 3  # gpt-4o, claude, gemini, gpt-4-turbo


def test_report_by_label(sample_entries):
    """Report breaks down by label correctly."""
    report = generate_cost_report(sample_entries)
    assert "chat" in report["by_label"]
    assert report["by_label"]["chat"]["calls"] == 3


def test_forecast_monthly_cost(sample_entries):
    """Forecast returns projections."""
    forecast = forecast_monthly_cost(sample_entries, days_in_window=7)
    assert forecast["daily_avg"] > 0
    assert forecast["monthly_projection"] > forecast["weekly_projection"]
    assert forecast["weekly_projection"] > forecast["daily_avg"]


def test_forecast_empty():
    """Forecast handles empty entries."""
    forecast = forecast_monthly_cost([], days_in_window=7)
    assert forecast["daily_avg"] == 0.0
    assert forecast["monthly_projection"] == 0.0


def test_check_budget_within(sample_entries):
    """Budget check when under budget."""
    result = check_budget(sample_entries, budget=100.0)
    assert not result["over_budget"]
    assert result["remaining"] > 0
    assert result["usage_percent"] < 100


def test_check_budget_over(sample_entries):
    """Budget check when over budget."""
    result = check_budget(sample_entries, budget=0.001)
    assert result["over_budget"]
    assert result["remaining"] < 0


def test_format_report_markdown(sample_entries):
    """Markdown report contains expected sections."""
    report = generate_cost_report(sample_entries)
    md = format_report_markdown(report)
    assert "# LLM Cost Report" in md
    assert "## Cost by Model" in md
    assert "## Cost by Provider" in md
    assert "gpt-4o" in md
