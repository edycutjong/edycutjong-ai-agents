import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.converter import RestToGraphqlConverter

@patch("agent.converter.GraphQLGenerator")
@patch("agent.converter.OpenAPIParser")
def test_convert(mock_parser, mock_generator):
    # Mock Parser
    parser_instance = mock_parser.return_value
    parser_instance.summarize.return_value = "API Summary"
    parser_instance.get_schemas.return_value = {"User": {}}
    parser_instance.get_paths.return_value = {"/users": {}}

    # Mock Generator
    generator_instance = mock_generator.return_value
    generator_instance.generate_types.return_value = "type User { id: ID }"
    generator_instance.generate_operations.return_value = "type Query { users: [User] }"
    generator_instance.generate_resolvers.return_value = "def resolve_users(): pass"
    generator_instance.generate_migration_guide.return_value = "# Migration Guide"

    converter = RestToGraphqlConverter(api_key="test-key")
    result = converter.convert('{"openapi": "3.0.0"}')

    assert result["schema"] == "type User { id: ID }\n\ntype Query { users: [User] }"
    assert result["resolvers"] == "def resolve_users(): pass"
    assert result["migration_guide"] == "# Migration Guide"

    # Verify calls
    mock_parser.assert_called_once_with('{"openapi": "3.0.0"}')
    generator_instance.generate_types.assert_called_once()
    generator_instance.generate_operations.assert_called_once()
    generator_instance.generate_resolvers.assert_called_once()
    generator_instance.generate_migration_guide.assert_called_once()
