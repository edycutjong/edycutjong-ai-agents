import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage
from agent.generator import TutorialGenerator

@patch("agent.generator.ChatOpenAI")
def test_generator_init(mock_chat):
    gen = TutorialGenerator(api_key="test")
    assert gen.llm is not None

@patch("agent.generator.ChatOpenAI")
def test_analyze_input_code(mock_chat):
    gen = TutorialGenerator(api_key="test")
    code = "def foo(): pass"
    context = gen.analyze_input(code, is_code=True)
    assert "Code Structure Analysis" in context
    assert "foo" in context

@patch("agent.generator.ChatOpenAI")
def test_generate_introduction(mock_chat):
    # Setup mock to return a valid message that StrOutputParser can handle
    mock_instance = mock_chat.return_value
    # Set invoke return value
    mock_instance.invoke.return_value = AIMessage(content="Generated Introduction")
    # Also set __call__ return value just in case LangChain uses that
    mock_instance.return_value = AIMessage(content="Generated Introduction")

    gen = TutorialGenerator(api_key="test")
    gen.context = "Context"

    result = gen.generate_introduction("Beginner")
    assert result == "Generated Introduction"

@patch("agent.generator.ChatOpenAI")
def test_generate_full_tutorial_stream(mock_chat):
    mock_instance = mock_chat.return_value
    mock_instance.invoke.return_value = AIMessage(content="Generated Content")
    mock_instance.return_value = AIMessage(content="Generated Content")

    gen = TutorialGenerator(api_key="test")

    # We need to mock analyze_text_content if input is text, or use code input
    code = "def foo(): pass"

    # Consume the generator
    sections = list(gen.generate_full_tutorial_stream(code, "Beginner", "Goal", is_code=True))

    assert len(sections) > 0
    names = [s[0] for s in sections]
    assert "Analysis" in names
    assert "Introduction" in names
    assert "Step-by-Step Guide" in names
