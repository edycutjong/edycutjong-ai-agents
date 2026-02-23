import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import argparse

# Add path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

class TestCLI(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.read_file')
    @patch('main.MigrationAgent')
    @patch('main.console')  # Mock rich console to suppress output
    def test_main_flow(self, mock_console, MockAgent, mock_read_file, mock_args):
        # Setup mocks
        mock_args.return_value = argparse.Namespace(
            old_schema="old.prisma",
            new_schema="new.prisma",
            orm="prisma",
            api_key="test-key"
        )
        mock_read_file.return_value = "schema content"

        mock_agent_instance = MagicMock()
        MockAgent.return_value = mock_agent_instance
        mock_agent_instance.generate_migration.return_value = "-- Migration"
        mock_agent_instance.generate_rollback.return_value = "-- Rollback"
        mock_agent_instance.analyze_safety.return_value = "Safe"

        # Run main
        main()

        # Assertions
        mock_read_file.assert_any_call("old.prisma")
        mock_read_file.assert_any_call("new.prisma")
        MockAgent.assert_called_with(api_key="test-key")
        mock_agent_instance.generate_migration.assert_called()
        mock_agent_instance.generate_rollback.assert_called()
        mock_agent_instance.analyze_safety.assert_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('main.console')
    def test_main_missing_file(self, mock_console, mock_file, mock_args):
        mock_args.return_value = argparse.Namespace(
            old_schema="missing.prisma",
            new_schema="new.prisma",
            orm="prisma",
            api_key="test-key"
        )

        # Mock sys.exit to raise SystemExit so main() stops
        with patch('sys.exit', side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):
                main()
            mock_exit.assert_called_with(1)
