import unittest
from unittest.mock import MagicMock, patch
import pytest

# Add path for local imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.migration_agent import MigrationAgent
from agent.schema_parser import parse_schema_text, validate_schema_input
from config import Config
from langchain_core.messages import AIMessage

class TestSchemaParser(unittest.TestCase):
    def test_parse_schema_text(self):
        self.assertEqual(parse_schema_text("  schema  "), "schema")
        self.assertEqual(parse_schema_text(""), "")
        self.assertEqual(parse_schema_text(None), "")

    def test_validate_schema_input(self):
        self.assertTrue(validate_schema_input("schema"))
        self.assertFalse(validate_schema_input(""))
        self.assertFalse(validate_schema_input(None))


class TestMigrationAgent(unittest.TestCase):
    @patch('agent.migration_agent.ChatOpenAI')
    def test_initialization_with_api_key(self, MockChatOpenAI):
        agent = MigrationAgent(api_key="test-key")
        self.assertIsNotNone(agent.llm)
        MockChatOpenAI.assert_called_once()

    @patch('agent.migration_agent.ChatOpenAI')
    def test_initialization_without_api_key(self, MockChatOpenAI):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with patch('config.Config.OPENAI_API_KEY', None):
                agent = MigrationAgent()
                self.assertIsNone(agent.llm)

    @patch('agent.migration_agent.ChatOpenAI')
    def test_generate_migration(self, MockChatOpenAI):
        mock_llm_instance = MagicMock()
        MockChatOpenAI.return_value = mock_llm_instance
        response_message = AIMessage(content="-- Migration SQL")
        mock_llm_instance.invoke.return_value = response_message
        mock_llm_instance.return_value = response_message

        agent = MigrationAgent(api_key="test-key")
        result = agent.generate_migration("old", "new", "prisma")
        self.assertEqual(result, "-- Migration SQL")

    @patch('agent.migration_agent.ChatOpenAI')
    def test_generate_rollback(self, MockChatOpenAI):
        mock_llm_instance = MagicMock()
        MockChatOpenAI.return_value = mock_llm_instance
        response_message = AIMessage(content="-- Rollback SQL")
        mock_llm_instance.invoke.return_value = response_message
        mock_llm_instance.return_value = response_message

        agent = MigrationAgent(api_key="test-key")
        result = agent.generate_rollback("-- Migration SQL", "prisma")
        self.assertEqual(result, "-- Rollback SQL")

    @patch('agent.migration_agent.ChatOpenAI')
    def test_analyze_safety(self, MockChatOpenAI):
        mock_llm_instance = MagicMock()
        MockChatOpenAI.return_value = mock_llm_instance
        response_message = AIMessage(content="Risk: Low")
        mock_llm_instance.invoke.return_value = response_message
        mock_llm_instance.return_value = response_message

        agent = MigrationAgent(api_key="test-key")
        result = agent.analyze_safety("-- Migration SQL", "old", "new")
        self.assertEqual(result, "Risk: Low")

    def test_methods_without_api_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with patch('config.Config.OPENAI_API_KEY', None):
                agent = MigrationAgent()
                self.assertIn("Error", agent.generate_migration("old", "new", "prisma"))
                self.assertIn("Error", agent.generate_rollback("code", "prisma"))
                self.assertIn("Error", agent.analyze_safety("code", "old", "new"))

    def test_unsupported_orm(self):
        agent = MigrationAgent(api_key="test-key")
        result = agent.generate_migration("old", "new", "unknown")
        self.assertIn("Error: Unsupported ORM", result)
