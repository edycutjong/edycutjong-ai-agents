import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from pydantic import BaseModel
from typing import List

# Mock Pydantic models to return from chains
class MockJobDescription(BaseModel):
    title: str = "Senior Developer"
    skills: List[str] = ["Python", "Django"]
    experience_level: str = "Senior"
    responsibilities: str = "Lead team"

class MockCodingQuestion(BaseModel):
    problem_statement: str = "Implement Fibonacci"
    examples: List[str] = ["fib(5) -> 5"]
    constraints: List[str] = ["O(n) time"]

class MockSystemDesignQuestion(BaseModel):
    prompt: str = "Design Twitter"
    requirements: List[str] = ["Scalable", "Reliable"]

class MockBehavioralQuestion(BaseModel):
    question: str = "Tell me about a time you failed."
    focus_area: str = "Failure"

class MockEvaluation(BaseModel):
    score: int = 8
    feedback: str = "Good job"
    improved_answer: str = "Better answer"

@pytest.fixture
def mock_llm():
    llm = MagicMock()  # pragma: no cover
    # default invoke behavior
    llm.invoke.return_value = AIMessage(content="Mock response")  # pragma: no cover
    return llm  # pragma: no cover

@pytest.fixture
def mock_chain():
    chain = MagicMock()  # pragma: no cover
    return chain  # pragma: no cover
