import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from agent.generator import QuestionGenerator, CodingQuestion, SystemDesignQuestion, BehavioralQuestion

@pytest.fixture
def mock_llm_response_coding():
    return '''
    {
        "problem_statement": "Implement Fibonacci",
        "examples": ["fib(5) -> 5"],
        "constraints": ["O(n) time"]
    }
    '''

@pytest.fixture
def mock_llm_response_system():
    return '''
    {
        "prompt": "Design Twitter",
        "requirements": ["Scalable", "Reliable"]
    }
    '''

@pytest.fixture
def mock_llm_response_behavioral():
    return '''
    {
        "question": "Tell me about a time you failed.",
        "focus_area": "Failure"
    }
    '''

def test_generate_coding_question(mock_llm_response_coding):
    fake_llm = RunnableLambda(lambda x: AIMessage(content=mock_llm_response_coding))

    with patch('agent.generator.ChatOpenAI') as mock_chat:
        generator = QuestionGenerator(api_key="fake")
        generator.llm = fake_llm

        result = generator.generate_coding_question(["Python"], "Mid", "Medium")

        assert result is not None
        assert result.problem_statement == "Implement Fibonacci"
        assert "fib(5) -> 5" in result.examples

def test_generate_system_design_question(mock_llm_response_system):
    fake_llm = RunnableLambda(lambda x: AIMessage(content=mock_llm_response_system))

    with patch('agent.generator.ChatOpenAI') as mock_chat:
        generator = QuestionGenerator(api_key="fake")
        generator.llm = fake_llm

        result = generator.generate_system_design_question(["Scalability"], "Senior")

        assert result is not None
        assert result.prompt == "Design Twitter"
        assert "Scalable" in result.requirements

def test_generate_behavioral_question(mock_llm_response_behavioral):
    fake_llm = RunnableLambda(lambda x: AIMessage(content=mock_llm_response_behavioral))

    with patch('agent.generator.ChatOpenAI') as mock_chat:
        generator = QuestionGenerator(api_key="fake")
        generator.llm = fake_llm

        result = generator.generate_behavioral_question("Failure")

        assert result is not None
        assert result.question == "Tell me about a time you failed."
        assert result.focus_area == "Failure"
