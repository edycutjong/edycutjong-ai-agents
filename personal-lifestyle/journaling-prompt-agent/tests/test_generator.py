import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agent.generator import PromptGenerator

@pytest.fixture
def mock_llm():
    with patch("agent.generator.ChatOpenAI") as mock:
        yield mock

def test_generator_init_no_key(monkeypatch):
    monkeypatch.setattr("agent.generator.OPENAI_API_KEY", None)
    generator = PromptGenerator()
    assert generator.api_key is None
    assert generator.llm is None

def test_generate_contextual_prompt_success(mock_llm, monkeypatch):
    # Mock API key to be present
    monkeypatch.setattr("agent.generator.OPENAI_API_KEY", "fake-key")

    generator = PromptGenerator()

    # Mock the chain invocation
    mock_instance = mock_llm.return_value
    # The chain is prompt | llm | parser.
    # invoke is called on the chain.
    # Implementation: chain = prompt | self.llm | StrOutputParser()
    # return chain.invoke(kwargs)

    # We need to mock the chain behavior.
    # Easier to mock `invoke` on the constructed chain, but the chain is constructed inside the method.
    # However, we can mock `ChatOpenAI` (which is self.llm) and verify it's used.
    # Actually, the implementation uses LCEL (LangChain Expression Language).

    # Let's mock the `_generate` method instead, since we want to test the `generate_*` methods wrapper logic?
    # Or we can mock `PromptTemplate.from_template` and the chain.

    with patch("agent.generator.PromptTemplate") as mock_prompt_cls:
        mock_prompt = MagicMock()
        mock_prompt_cls.from_template.return_value = mock_prompt

        # chain = prompt | llm | parser
        # We can simulate the chain using magic mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Generated Prompt"

        # When we pipe, it returns a new object.
        # prompt | llm -> pipe1
        # pipe1 | parser -> chain

        # This is getting complicated to mock accurately with LCEL.
        # Simpler approach: Mock `_generate` method to return a string.
        # This tests that `generate_contextual_prompt` calls `_generate` with correct template and args.

        with patch.object(generator, "_load_prompt", return_value="Mock Template") as mock_load:
            with patch.object(generator, "_generate", return_value="Mocked Prompt") as mock_generate:
                result = generator.generate_contextual_prompt("Happy", 8, "Context")

                assert result == "Mocked Prompt"
                mock_load.assert_called_with("contextual.txt")
                mock_generate.assert_called_once()
                call_args = mock_generate.call_args
                assert call_args[0][0] == "Mock Template"

def test_load_prompt_and_generate_flow(monkeypatch):
    monkeypatch.setattr("agent.generator.OPENAI_API_KEY", "fake-key")
    generator = PromptGenerator()

    # Mock _load_prompt to return a simple string
    with patch.object(generator, "_load_prompt", return_value="Template {mood}") as mock_load:
        # Mock LLM chain execution
        # Instead of full LCEL mock, let's just see if it doesn't crash and tries to use LLM.
        # But `_generate` tries to use `self.llm`. `self.llm` is a MagicMock (from class patch if we used it, but here we manually instantiated).

        # Let's mock `ChatOpenAI` class so `self.llm` is a mock.
        with patch("agent.generator.ChatOpenAI"):
            generator = PromptGenerator() # re-init to pick up mock

            # Now mock the chain behavior inside _generate?
            # Or just rely on the fact that if we don't mock the chain, it might fail or try to connect.
            # But `ChatOpenAI` is mocked, so it won't connect.
            # However, `PromptTemplate.from_template("Template {mood}")` works.
            # `prompt | self.llm` works (returns runnable).
            # `runnable | StrOutputParser()` works.
            # `chain.invoke` calls `invoke` on pipeline.
            # Eventually it calls `self.llm.invoke`.
            # Since `self.llm` is a Mock, it should return a Mock.
            # `StrOutputParser` expects a string or message. Mock object might not behave like a message.

            # So we should configure the mock LLM to return a message-like object or string.
            mock_llm_instance = generator.llm
            # ChatOpenAI returns an AIMessage.
            from langchain_core.messages import AIMessage
            mock_llm_instance.invoke.return_value = AIMessage(content="AI Generated")

            # Wait, LCEL passes inputs differently.
            # But let's just try mocking `_generate` for the public methods, and test `_generate` separately if needed.
            pass

    # Let's stick to testing logic:
    # 1. generate_contextual_prompt calls _load_prompt with correct file.
    # 2. generate_contextual_prompt calls _generate with correct args.

    with patch.object(generator, "_load_prompt", return_value="Template") as mock_load:
        with patch.object(generator, "_generate", return_value="Result") as mock_gen:
            generator.generate_contextual_prompt("Sad", 2, "Tired")
            mock_load.assert_called_with("contextual.txt")
            mock_gen.assert_called_with("Template", mood="Sad", energy=2, context="Tired")

def test_generate_no_api_key():
    generator = PromptGenerator()
    generator.llm = None # Ensure no LLM

    result = generator._generate("template")
    assert "Error: OpenAI API Key not found" in result
