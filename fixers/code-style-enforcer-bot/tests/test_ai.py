from tools.ai import ai_helper
from unittest.mock import MagicMock

def test_ai_mock_behavior():
    # Force mock mode
    ai_helper.llm = None

    explanation = ai_helper.explain_rule("E501", "Line too long")
    assert "Mocked AI explanation" in explanation

    vibe = ai_helper.check_vibe("print('hello')")
    assert "Mocked AI vibe check" in vibe

    learn = ai_helper.learn_from_codebase("def foo(): pass")
    assert "Mocked" in learn

def test_ai_with_mock_llm():
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "This is a real AI response"

    # LangChain might call the object directly (if treated as callable) or .invoke()
    mock_llm.return_value = mock_response
    mock_llm.invoke.return_value = mock_response

    ai_helper.llm = mock_llm

    explanation = ai_helper.explain_rule("E501", "Line too long")

    # Verify the interaction
    assert explanation == "This is a real AI response"
