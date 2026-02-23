import pytest
from unittest.mock import MagicMock, patch
from agent.parser import JobParser, JobDescription
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

def test_parser_mock_chain():
    # Setup expected JSON response from LLM
    json_response = '''
    {
        "title": "Senior Python Developer",
        "skills": ["Python", "Django", "AWS"],
        "experience_level": "Senior",
        "responsibilities": "Lead backend development"
    }
    '''

    # Create a Fake LLM using RunnableLambda that returns an AIMessage
    fake_llm = RunnableLambda(lambda x: AIMessage(content=json_response))

    # Patch ChatOpenAI in JobParser initialization to avoid real API calls,
    # but we will overwrite self.llm anyway.
    with patch('agent.parser.ChatOpenAI') as mock_chat:
        parser = JobParser(api_key="fake")
        # Replace the mocked LLM with our functioning Fake LLM Runnable
        parser.llm = fake_llm

        # Run parse
        result = parser.parse("Need a python dev")

        # Assertions
        assert result is not None
        assert result.title == "Senior Python Developer"
        assert "Django" in result.skills
        assert result.experience_level == "Senior"
