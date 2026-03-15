"""Tests for main.py CLI."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_create, cmd_list, cmd_show
from config import Config

def test_config(): assert Config is not None

def test_cmd_create(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'from_name': 'Co', 'to_name': 'Client', 'currency': 'USD', 'notes': 'Thanks', 'items': ['Item,10,2,0.1'], 'markdown': False, 'json': False})()
        with patch("builtins.print") as p: cmd_create(args)

def test_cmd_create_markdown(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'from_name': 'Co', 'to_name': 'Client', 'currency': 'USD', 'notes': '', 'items': ['Item,10,2'], 'markdown': True, 'json': False})()
        with patch("builtins.print") as p: cmd_create(args)

def test_cmd_create_json(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'from_name': 'Co', 'to_name': 'Client', 'currency': 'USD', 'notes': '', 'items': ['Item,10,2'], 'markdown': False, 'json': True})()
        with patch("builtins.print") as p: cmd_create(args)

def test_cmd_list(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'status': None, 'json': False})()
        with patch("builtins.print") as p: cmd_list(args)

def test_cmd_show(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'number': 'INV-0001'})()
        with patch("builtins.print") as p:
            with pytest.raises(SystemExit):
                cmd_show(args)

def test_cmd_show_success(tmp_path):
    from agent.invoice import Invoice
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        inv = Invoice("A", "B", "USD", "")
        with patch("agent.invoice.InvoiceStorage.get_by_number", return_value=inv):
            args_md = type('A', (), {'number': inv.invoice_number, 'markdown': True})()
            args_txt = type('A', (), {'number': inv.invoice_number, 'markdown': False})()
            with patch("builtins.print"): cmd_show(args_md)
            with patch("builtins.print"): cmd_show(args_txt)

def test_main_create(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        with patch("sys.argv", ["main", "create", "--items", "Svc,100,1"]):
            with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        with patch("sys.argv", ["main", "list"]):
            with patch("builtins.print"):
                with patch.dict("sys.modules", {"__main__": None}):
                    runpy.run_module("main", run_name="__main__", alter_sys=True)
