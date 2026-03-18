import pytest
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from agent.grader import ResponseGrader, Evaluation

import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_builtin_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "dummy")


@pytest.fixture
def mock_llm_response_evaluation():
    return '''
    {
        "score": 8,
        "feedback": "Good job, but consider edge cases.",
        "improved_answer": "Check for null input first."
    }
    '''

def test_grade_response(mock_llm_response_evaluation):
    fake_llm = RunnableLambda(lambda x: AIMessage(content=mock_llm_response_evaluation))

    with patch('agent.grader.ChatOpenAI') as mock_chat:
        grader = ResponseGrader(api_key="fake")
        grader.llm = fake_llm

        result = grader.grade_response("Implement fib", "def fib(n): return n", "Coding")

        assert result is not None
        assert result.score == 8
        assert "Good job" in result.feedback
        assert "Check for null" in result.improved_answer
