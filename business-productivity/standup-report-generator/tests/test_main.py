"""Tests for main.py CLI."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_add, cmd_daily, cmd_weekly, cmd_blockers
from config import Config

def test_config(): assert Config is not None

def test_cmd_add(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'author': 'Dev', 'yesterday': 'Fixed bugs;Reviewed PRs', 'today': 'Build feature', 'blockers': '', 'tags': 'sprint-1', 'mood': 'good'})()
        with patch("builtins.print") as p: cmd_add(args)

def test_cmd_daily(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'date': None})()
        with patch("builtins.print") as p: cmd_daily(args)

def test_cmd_weekly(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'author': None})()
        with patch("builtins.print") as p: cmd_weekly(args)

def test_cmd_blockers(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args = type('A', (), {'days': 7})()
        with patch("builtins.print") as p: cmd_blockers(args)

def test_main_add(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        with patch("sys.argv", ["main", "add", "--author", "Dev", "--today", "coding"]):
            with patch("builtins.print"): main()

def test_cmd_list(tmp_path):
    from main import cmd_list, StandupEntry
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        args1 = type('A', (), {'author': None})()
        args2 = type('A', (), {'author': 'Dev'})()
        
        # add a mock entry so we hit the loop body and blockers condition
        storage_mock = patch("main.StandupStorage").start()
        instance = storage_mock.return_value
        entry1 = StandupEntry(author="Dev", yesterday=[], today=["Task 1"], blockers=["Blocker"], tags=[], mood="")
        entry2 = StandupEntry(author="Other", yesterday=[], today=["Task 2"], blockers=[], tags=[], mood="")
        
        instance.get_all.return_value = [entry1, entry2]
        instance.get_by_author.return_value = [entry1]
        
        with patch("builtins.print"):
            cmd_list(args1)
            cmd_list(args2)
        patch.stopall()


def test_main_entry_point(tmp_path):
    with patch.dict(os.environ, {"HOME": str(tmp_path)}):
        with patch("sys.argv", ["main", "daily"]):
            with patch("builtins.print"):
                with patch.dict("sys.modules", {"__main__": None}):
                    runpy.run_module("main", run_name="__main__", alter_sys=True)
