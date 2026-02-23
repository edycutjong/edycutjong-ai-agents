import pytest
import sys
import os

# Adjust path to import tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.ast_parser import CodeScanner

def test_scan_file(tmp_path):
    py_file = tmp_path / "app.py"
    py_file.write_text("""
import logging

def main():
    print("Hello world")
    logging.info(f"Processing item {item}")
    logging.error("Static error")
    """, encoding='utf-8')

    scanner = CodeScanner(str(tmp_path))
    findings = scanner.scan()

    assert len(findings) == 3

    # Check print
    print_findings = [f for f in findings if f['type'] == 'print']
    assert len(print_findings) == 1
    assert print_findings[0]['line'] == 5
    assert print_findings[0]['message_template'] == "Hello world"

    # Check logging.info
    info_findings = [f for f in findings if f['type'] == 'logging.info']
    assert len(info_findings) == 1
    assert info_findings[0]['line'] == 6
    assert "Processing item <VAR>" in info_findings[0]['message_template']

    # Check logging.error
    error_findings = [f for f in findings if f['type'] == 'logging.error']
    assert len(error_findings) == 1
    assert error_findings[0]['line'] == 7
    assert error_findings[0]['message_template'] == "Static error"
