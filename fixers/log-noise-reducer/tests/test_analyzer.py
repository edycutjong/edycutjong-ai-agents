import pytest
import sys
import os

# Adjust path to import tools
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.log_analyzer import LogAnalyzer

def test_normalize_line():
    analyzer = LogAnalyzer("dummy.log")

    # The normalizer might produce extra spaces depending on regex.
    # "<TIMESTAMP> INFO Processing item <NUM>"
    normalized = analyzer._normalize_line("2023-10-27 10:00:00 INFO Processing item 1")
    assert "INFO Processing item <NUM>" in normalized
    assert "<TIMESTAMP>" in normalized

    assert "User <NUM> logged in" in analyzer._normalize_line("User 123 logged in")
    assert "Connection from <IP>" in analyzer._normalize_line("Connection from 192.168.1.1")

def test_analyze_file(tmp_path):
    log_file = tmp_path / "test.log"
    content = "2023-01-01 10:00:00 INFO Processing item 1\n2023-01-01 10:00:01 INFO Processing item 2\n2023-01-01 10:00:02 ERROR Failed\n"
    log_file.write_text(content, encoding='utf-8')

    analyzer = LogAnalyzer(str(log_file))
    analyzer.read_logs()
    patterns = analyzer.analyze()

    assert len(patterns) == 2
    # First pattern should be the INFO one with count 2
    # Pattern: "<TIMESTAMP> INFO Processing item <NUM>"
    assert patterns[0][1] == 2
    assert "INFO Processing item <NUM>" in patterns[0][0]

    # Second pattern ERROR with count 1
    assert patterns[1][1] == 1
    assert "ERROR Failed" in patterns[1][0]
