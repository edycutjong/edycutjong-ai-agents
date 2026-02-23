import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.suggester import Suggester

def test_suggester():
    log_counts = [
        ("Processing item <NUM>", 100),
        ("Error occurred", 10)
    ]
    code_findings = [
        {"file": "app.py", "line": 10, "type": "logging.info", "message_template": "Processing item <VAR>"},
        {"file": "app.py", "line": 20, "type": "logging.error", "message_template": "Error occurred"}
    ]
    total_logs = 110

    suggester = Suggester(log_counts, code_findings, total_logs)
    suggestions = suggester.generate_suggestions()

    assert len(suggestions) == 2

    # First suggestion: INFO log with 90% volume
    assert suggestions[0]['pattern'] == "Processing item <NUM>"
    assert suggestions[0]['count'] == 100
    assert suggestions[0]['percentage'] > 90
    assert suggestions[0]['action'] == "Change to Debug"
    assert suggestions[0]['severity'] == "Medium"

    # Second suggestion: ERROR log with ~9% volume
    assert suggestions[1]['pattern'] == "Error occurred"
    assert suggestions[1]['count'] == 10
    assert suggestions[1]['action'] == "Investigate"
    assert suggestions[1]['severity'] == "Low"
