import pytest
from unittest.mock import patch
import sys
import os

# Minimal integration test to ensuring the agent runs and handles arguments
def test_agent_main_dry_run():
    # We need to make sure 'agent' is importable.
    # Since we set PYTHONPATH to include apps/agents/fixers/doc-drift-fixer,
    # we can import agent directly.

    with patch('sys.argv', ['agent.py', '--dry-run']), \
         patch('agent.GitHandler') as MockGit, \
         patch('agent.CodeAnalyzer'), \
         patch('agent.DocManager'), \
         patch('agent.DocGenerator'):

        import agent
        from agent import main

        MockGit.return_value.list_changed_files.return_value = []

        # Should run without error and print "No code changes detected"
        main()
