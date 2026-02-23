import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Fix path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.models import UserProfile, WorkoutPlan
from agent.generator import generate_workout_plan

@patch('agent.generator.ChatOpenAI')
@patch('agent.generator.get_workout_prompt')
@patch('agent.generator.OPENAI_API_KEY', "fake-key")
def test_generate_workout_plan(mock_get_prompt, mock_chat_openai):
    # Mock user profile
    profile = UserProfile(
        name="Test", age=25, weight=70, height=175,
        fitness_goal="General", fitness_level="Beginner",
        equipment=["None"], days_per_week=3, duration_per_session=30
    )

    # Mock prompt
    mock_prompt = MagicMock()
    mock_get_prompt.return_value = mock_prompt

    # Mock LLM and Structured LLM
    mock_llm = MagicMock()
    mock_chat_openai.return_value = mock_llm

    mock_structured_llm = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured_llm

    # Mock the chain: prompt | structured_llm
    mock_chain = MagicMock()
    mock_prompt.__or__.return_value = mock_chain

    # Mock chain result
    expected_plan = WorkoutPlan(
        plan_name="Test Plan",
        weeks=[],
        difficulty_progression="None",
        equipment_needed=[]
    )
    mock_chain.invoke.return_value = expected_plan

    # Execute
    result = generate_workout_plan(profile)

    # Assert
    assert result == expected_plan
    mock_chain.invoke.assert_called_once()
