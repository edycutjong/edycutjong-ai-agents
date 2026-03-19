import pytest
from unittest.mock import MagicMock, patch
import json
import sys
import os
from main import (
    cmd_calc, cmd_compare, cmd_cheapest, cmd_log, cmd_report,
    cmd_forecast, cmd_budget, cmd_models, cmd_providers, main
)
from agent.storage import UsageStorage
from agent.calculator import UsageEntry
from datetime import datetime

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_cmd_calc(capsys):
    args = DummyArgs(model="gpt-4o", input_tokens=1000, output_tokens=500)
    cmd_calc(args)
    captured = capsys.readouterr()
    assert "gpt-4o" in captured.out
    assert "Total Cost" in captured.out

def test_cmd_calc_error(capsys):
    args = DummyArgs(model="nonexistent-model", input_tokens=1000, output_tokens=500)
    cmd_calc(args)
    captured = capsys.readouterr()
    assert "Error" in captured.err

def test_cmd_compare(capsys):
    args = DummyArgs(input_tokens=1000, output_tokens=500)
    cmd_compare(args)
    captured = capsys.readouterr()
    assert "Cost comparison" in captured.out
    assert "gpt-4o" in captured.out

def test_cmd_cheapest(capsys):
    args = DummyArgs(model="gpt-4o")
    cmd_cheapest(args)
    captured = capsys.readouterr()
    assert "Cheaper alternatives to gpt-4o" in captured.out

@patch("main.find_cheapest_alternative", return_value=[])
def test_cmd_cheapest_none(mock_find, capsys):
    args = DummyArgs(model="gpt-4o-mini")
    cmd_cheapest(args)
    captured = capsys.readouterr()
    assert "No cheaper alternatives found for gpt-4o-mini." in captured.out

def test_cmd_log(capsys):
    storage_temp = os.path.join(os.path.dirname(__file__), "temp_storage.json")
    try:
        with patch("agent.storage.Config.STORAGE_FILE", storage_temp):
            args = DummyArgs(model="gpt-4o", input_tokens=1000, output_tokens=500, label="test-label")
            cmd_log(args)
            captured = capsys.readouterr()
            assert "test-label" in captured.out
    finally:
        if os.path.exists(storage_temp):
            os.remove(storage_temp)

def test_cmd_report_empty(capsys):
    storage_temp = os.path.join(os.path.dirname(__file__), "temp_storage_empty.json")
    try:
        with patch("agent.storage.Config.STORAGE_FILE", storage_temp):
            args = DummyArgs(markdown=False)
            cmd_report(args)
            captured = capsys.readouterr()
            assert "No usage data logged yet" in captured.out
    finally:
        if os.path.exists(storage_temp):
            os.remove(storage_temp)

def test_cmd_report(capsys):
    storage_temp = os.path.join(os.path.dirname(__file__), "temp_storage_rep.json")
    try:
        with patch("agent.storage.Config.STORAGE_FILE", storage_temp):
            storage = UsageStorage()
            storage.add_entry(UsageEntry(model="gpt-4o", input_tokens=100, output_tokens=100, timestamp=datetime.now().isoformat(), label=""))
            args = DummyArgs(markdown=False)
            cmd_report(args)
            captured = capsys.readouterr()
            assert "Total Cost" in captured.out
            assert "gpt-4o" in captured.out
            
            args = DummyArgs(markdown=True)
            cmd_report(args)
            captured2 = capsys.readouterr()
            assert "# LLM Cost Report" in captured2.out
    finally:
        if os.path.exists(storage_temp):
            os.remove(storage_temp)

def test_cmd_forecast_empty(capsys):
    storage_temp = os.path.join(os.path.dirname(__file__), "temp_storage_f_empty.json")
    try:
        with patch("agent.storage.Config.STORAGE_FILE", storage_temp):
            args = DummyArgs(days=7)
            cmd_forecast(args)
            captured = capsys.readouterr()
            assert "No usage data logged yet" in captured.out
    finally:
        if os.path.exists(storage_temp):
            os.remove(storage_temp)

def test_cmd_forecast(capsys):
    storage_temp = os.path.join(os.path.dirname(__file__), "temp_storage_f.json")
    try:
        with patch("agent.storage.Config.STORAGE_FILE", storage_temp):
            storage = UsageStorage()
            storage.add_entry(UsageEntry(model="gpt-4o", input_tokens=1000, output_tokens=500, timestamp=datetime.now().isoformat(), label=""))
            args = DummyArgs(days=7)
            cmd_forecast(args)
            captured = capsys.readouterr()
            assert "Forecast" in captured.out
            assert "Monthly projection" in captured.out
    finally:
        if os.path.exists(storage_temp):
            os.remove(storage_temp)

def test_cmd_budget(capsys):
    storage_temp = os.path.join(os.path.dirname(__file__), "temp_storage_b.json")
    try:
        with patch("agent.storage.Config.STORAGE_FILE", storage_temp):
            storage = UsageStorage()
            storage.add_entry(UsageEntry(model="gpt-4o", input_tokens=1000000, output_tokens=500000, timestamp=datetime.now().isoformat(), label=""))
            args = DummyArgs(amount=1.0) # small budget
            cmd_budget(args)
            captured = capsys.readouterr()
            assert "Budget Check" in captured.out
            assert "OVER BUDGET" in captured.out
    finally:
        if os.path.exists(storage_temp):
            os.remove(storage_temp)

def test_cmd_models(capsys):
    args = DummyArgs()
    cmd_models(args)
    captured = capsys.readouterr()
    assert "gpt-4o" in captured.out
    assert "Total:" in captured.out

def test_cmd_providers(capsys):
    args = DummyArgs()
    cmd_providers(args)
    captured = capsys.readouterr()
    assert "Anthropic" in captured.out or "OpenAI" in captured.out
    assert "models):" in captured.out

def test_storage_create_dir(tmp_path):
    nested_file = tmp_path / "new_dir" / "test.json"
    storage = UsageStorage(str(nested_file))
    assert os.path.exists(tmp_path / "new_dir")
    assert os.path.exists(nested_file)

@patch("sys.argv", ["main.py", "models"])
def test_main_cli(capsys):
    main()
    captured = capsys.readouterr()
    assert "gpt-4o" in captured.out
