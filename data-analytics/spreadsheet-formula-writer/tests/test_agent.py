import pytest
from unittest.mock import MagicMock
from agent.core import FormulaWriterAgent
from agent.models import FormulaResponse

@pytest.fixture
def mock_llm_chain(mocker):
    # Mock API Key
    mocker.patch("agent.core.OPENAI_API_KEY", "test-key")

    # Mock ChatOpenAI class
    mock_llm_cls = mocker.patch("agent.core.ChatOpenAI")

    # Mock the LLM instance
    mock_llm_instance = mock_llm_cls.return_value

    # Mock with_structured_output which returns the structured LLM runnable
    mock_structured_runnable = MagicMock()
    mock_llm_instance.with_structured_output.return_value = mock_structured_runnable

    expected_response = FormulaResponse(
        formula="=SUM(A:A)",
        explanation="Sums all values in column A.",
        alternatives=["=SUM(A1:A100)"],
        examples=["If A1=5, A2=10, result is 15"]
    )

    # Set return value for invoke
    mock_structured_runnable.invoke.return_value = expected_response
    # Also set return value for direct call (if wrapped as lambda)
    mock_structured_runnable.return_value = expected_response

    return mock_llm_cls, mock_structured_runnable

def test_generate_formula_success(mock_llm_chain):
    mock_llm_cls, mock_structured_runnable = mock_llm_chain

    agent = FormulaWriterAgent(model_name="gpt-4o")
    response = agent.generate_formula("Sum column A")

    assert isinstance(response, FormulaResponse)
    assert response.formula == "=SUM(A:A)"
    assert response.explanation == "Sums all values in column A."
    assert response.alternatives == ["=SUM(A1:A100)"]
    assert response.examples == ["If A1=5, A2=10, result is 15"]

    # Verify mock calls
    mock_llm_cls.assert_called_once()
    # It might be called via invoke or __call__, check either
    assert mock_structured_runnable.invoke.called or mock_structured_runnable.called

def test_generate_formula_error(mocker):
    # Mock API Key
    mocker.patch("agent.core.OPENAI_API_KEY", "test-key")

    # Mock ChatOpenAI class
    mock_llm_cls = mocker.patch("agent.core.ChatOpenAI")
    mock_llm_instance = mock_llm_cls.return_value
    mock_structured_runnable = MagicMock()
    mock_llm_instance.with_structured_output.return_value = mock_structured_runnable

    # Raise error on invoke and call
    mock_structured_runnable.invoke.side_effect = Exception("API Error")
    mock_structured_runnable.side_effect = Exception("API Error")

    agent = FormulaWriterAgent()

    # We need to ensure we bypass retry for this test to be fast, or assume it retries 3 times then fails.
    # The default retry in core.py is 3 attempts.

    # But wait, we need to mock the chain creation so we can control invoke side effects on the CHAIN, not just LLM.
    # Because generate_formula creates 'chain = prompt | structured_llm'

    mock_get_prompt = mocker.patch("agent.core.get_formula_prompt")
    mock_prompt = MagicMock()
    mock_get_prompt.return_value = mock_prompt

    mock_chain = MagicMock()
    # If prompt | llm is called, return mock_chain
    mock_prompt.__or__.return_value = mock_chain

    mock_chain.invoke.side_effect = Exception("API Error")

    with pytest.raises(RuntimeError, match="Failed to generate formula: API Error"):
        agent.generate_formula("Sum column A")

    # Should have been called 3 times due to retry
    assert mock_chain.invoke.call_count == 3


def test_generate_formula_retry_success(mocker):
    # Mock API Key
    mocker.patch("agent.core.OPENAI_API_KEY", "test-key")

    # Mock ChatOpenAI class
    mock_llm_cls = mocker.patch("agent.core.ChatOpenAI")

    expected_response = FormulaResponse(
        formula="=SUM(A:A)",
        explanation="Sums column A",
        alternatives=[],
        examples=[]
    )

    # Mock chain creation
    mock_get_prompt = mocker.patch("agent.core.get_formula_prompt")
    mock_prompt = MagicMock()
    mock_get_prompt.return_value = mock_prompt

    mock_chain = MagicMock()
    mock_prompt.__or__.return_value = mock_chain

    # Fail first, then succeed
    mock_chain.invoke.side_effect = [Exception("Temporary Error"), expected_response]

    agent = FormulaWriterAgent()
    response = agent.generate_formula("query")

    assert response == expected_response
    assert mock_chain.invoke.call_count == 2


def test_init_raises_if_no_api_key(mocker):
    # Mock config import where OPENAI_API_KEY is imported
    # We patch 'agent.core.OPENAI_API_KEY'
    mocker.patch("agent.core.OPENAI_API_KEY", None)

    with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
        FormulaWriterAgent()

def test_init_with_explicit_api_key(mocker):
    # Mock config OPENAI_API_KEY as None to ensure explicit key is used
    mocker.patch("agent.core.OPENAI_API_KEY", None)

    # Mock ChatOpenAI to verify it receives the key
    mock_llm_cls = mocker.patch("agent.core.ChatOpenAI")

    agent = FormulaWriterAgent(api_key="explicit-key")

    mock_llm_cls.assert_called_with(
        model="gpt-4o",
        temperature=0.0,
        api_key="explicit-key"
    )
    assert agent.api_key == "explicit-key"
