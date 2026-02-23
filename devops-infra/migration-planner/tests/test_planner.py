import pytest
import sys
import os
import json
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage

# Append path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agent.planner import MigrationPlanner
from agent.models import MigrationPlan, BreakingChange, DataIntegrityCheck

@patch('agent.planner.ChatOpenAI')
@patch('agent.planner.ChatGoogleGenerativeAI')
def test_generate_plan_and_helpers(mock_gemini, mock_openai):
    # Setup mock LLM instance
    mock_llm_instance = MagicMock()
    mock_openai.return_value = mock_llm_instance

    # Mock the response from LLM
    response_data = {
        "steps": [
            {
                "id": 1,
                "description": "Create table users",
                "sql_up": "CREATE TABLE users (id INT PRIMARY KEY);",
                "sql_down": "DROP TABLE users;",
                "risk_level": "low",
                "estimated_duration_seconds": 10
            }
        ],
        "breaking_changes": [
            {
                "description": "Drop column email",
                "impact": "Data loss",
                "mitigation": "Backup before running"
            }
        ],
        "integrity_checks": [
            {
                "description": "Check user count",
                "query": "SELECT COUNT(*) FROM users",
                "expected_result": "0"
            }
        ],
        "total_estimated_duration_seconds": 10,
        "summary": "Create users table"
    }

    json_response = json.dumps(response_data)
    ai_message = AIMessage(content=json_response)

    mock_llm_instance.invoke.return_value = ai_message
    mock_llm_instance.return_value = ai_message

    # Mock config
    with patch('agent.planner.config') as mock_config:
        mock_config.LLM_PROVIDER = "openai"
        mock_config.OPENAI_API_KEY = "test-key"
        mock_config.MODEL_NAME = "gpt-4"
        mock_config.TEMPERATURE = 0.2

        planner = MigrationPlanner()

        # Call generate_plan
        plan = planner.generate_plan("CREATE TABLE foo", "CREATE TABLE foo (id INT)")

        # Verify the result is a MigrationPlan object
        assert isinstance(plan, MigrationPlan)

        # Verify helper methods
        sql_script = planner.generate_sql_script(plan)
        assert "CREATE TABLE users" in sql_script
        assert "-- Step 1: Create table users" in sql_script

        rollback_script = planner.generate_rollback_script(plan)
        assert "DROP TABLE users" in rollback_script
        assert "-- Revert Step 1: Create table users" in rollback_script

        breaking = planner.identify_breaking_changes(plan)
        assert len(breaking) == 1
        assert breaking[0].description == "Drop column email"

        integrity = planner.validate_data_integrity(plan)
        assert len(integrity) == 1
        assert integrity[0].query == "SELECT COUNT(*) FROM users"
