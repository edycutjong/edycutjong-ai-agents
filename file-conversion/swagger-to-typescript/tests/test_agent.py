import pytest
from unittest.mock import patch, MagicMock
from agent.core import generate_typescript
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

@patch('agent.core.ChatOpenAI')
def test_generate_typescript(mock_chat):
    # Create a fake LLM that returns a valid AIMessage
    def fake_llm_func(input):
        return AIMessage(content="```typescript\nconsole.log('success');\n```")

    # Mock ChatOpenAI to return a RunnableLambda wrapping our fake function
    # We use side_effect to handle instantiation
    mock_chat.side_effect = lambda **kwargs: RunnableLambda(fake_llm_func)

    spec = {"openapi": "3.0.0"}

    # Run the function
    result = generate_typescript(spec, api_key="test_key")

    # Verify the output
    assert "console.log('success');" in result
    assert "typescript" not in result # Should be stripped
