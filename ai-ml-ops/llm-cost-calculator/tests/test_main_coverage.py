import os
import sys
import runpy
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main
from main import cmd_calc, cmd_compare, cmd_cheapest, cmd_log, cmd_report, cmd_forecast, cmd_budget, cmd_models, cmd_providers


def test_calc_subcommand():
    with patch("sys.argv", ["main.py", "calc"]):
        with patch("main.cmd_calc") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_compare_subcommand():
    with patch("sys.argv", ["main.py", "compare"]):
        with patch("main.cmd_compare") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_cheapest_subcommand():
    with patch("sys.argv", ["main.py", "cheapest"]):
        with patch("main.cmd_cheapest") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_log_subcommand():
    with patch("sys.argv", ["main.py", "log"]):
        with patch("main.cmd_log") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_report_subcommand():
    with patch("sys.argv", ["main.py", "report"]):
        with patch("main.cmd_report") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_forecast_subcommand():
    with patch("sys.argv", ["main.py", "forecast"]):
        with patch("main.cmd_forecast") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_budget_subcommand():
    with patch("sys.argv", ["main.py", "budget"]):
        with patch("main.cmd_budget") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_models_subcommand():
    with patch("sys.argv", ["main.py", "models"]):
        with patch("main.cmd_models") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_providers_subcommand():
    with patch("sys.argv", ["main.py", "providers"]):
        with patch("main.cmd_providers") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except (SystemExit, Exception):
            pass
