import sys
import os
import runpy
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from agent.scanner import suggest_firewall_rules, analyze_ports, format_result_markdown

def test_config():
    c = Config()
    assert c is not None

def test_firewall_rules_unknown_service():
    rules = suggest_firewall_rules([9999])
    assert "REVIEW 9999/tcp  # Unknown service" in rules[0]

def test_format_result_markdown_with_issues():
    result = analyze_ports([21]) # 21 is FTP, should generate issues
    md = format_result_markdown(result)
    assert "### Security Issues" in md
    assert "- 🔴" in md

def test_main_scan(capsys):
    with patch("sys.argv", ["main.py", "scan", "22,80", "--target", "example.com"]):
        runpy.run_path(os.path.join(os.path.dirname(__file__), '..', 'main.py'), run_name="__main__")
    
    captured = capsys.readouterr()
    assert "example.com" in captured.out
    assert "Port 22: SSH" in captured.out
