import sys
from unittest.mock import MagicMock, patch

# Mock dependencies before import
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_google_genai'] = MagicMock()
sys.modules['langchain_core'] = MagicMock()
sys.modules['langchain_core.prompts'] = MagicMock()
sys.modules['langchain_core.output_parsers'] = MagicMock()
sys.modules['fpdf'] = MagicMock()
sys.modules['streamlit'] = MagicMock()

# Now import the module under test
from agent.core import PressReleaseGenerator

def test_initialization():
    """Test that the generator initializes correctly with default provider."""
    # Mock Config
    with patch('agent.core.Config') as MockConfig:
        MockConfig.DEFAULT_MODEL_PROVIDER = 'openai'
        MockConfig.OPENAI_API_KEY = 'test_key'

        # Mock ChatOpenAI
        with patch('agent.core.ChatOpenAI') as MockChatOpenAI:
            agent = PressReleaseGenerator()
            MockChatOpenAI.assert_called_once()
            assert agent.llm is not None

def test_generate_release():
    """Test generating a press release."""
    with patch('agent.core.Config') as MockConfig, \
         patch('agent.core.ChatOpenAI'), \
         patch('agent.core.ChatPromptTemplate') as MockPrompt, \
         patch('agent.core.StrOutputParser') as MockParser:

        # Configure Config Mock
        MockConfig.DEFAULT_MODEL_PROVIDER = 'openai'
        MockConfig.OPENAI_API_KEY = 'test'

        agent = PressReleaseGenerator()

        # Mock the chain
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Press Release Content"

        # Mock objects
        mock_prompt_instance = MockPrompt.from_messages.return_value
        mock_llm_instance = agent.llm
        mock_parser_instance = MockParser.return_value

        # Mock piping: prompt | llm -> intermediate
        mock_intermediate = MagicMock()
        mock_prompt_instance.__or__.return_value = mock_intermediate

        # intermediate | parser -> chain
        mock_chain_instance = MagicMock()
        mock_intermediate.__or__.return_value = mock_chain_instance

        mock_chain_instance.invoke.return_value = "Generated Release"

        result = agent.generate_release(
            "Product", "Details", "Company", "Desc", "Person", "Media", "Audience", "Tone"
        )

        assert result == "Generated Release"
        mock_chain_instance.invoke.assert_called_once()

def test_generate_quotes():
    with patch('agent.core.Config') as MockConfig, \
         patch('agent.core.ChatOpenAI'), \
         patch('agent.core.ChatPromptTemplate') as MockPrompt:

        MockConfig.DEFAULT_MODEL_PROVIDER = 'openai'
        MockConfig.OPENAI_API_KEY = 'test'

        agent = PressReleaseGenerator()

        mock_prompt_instance = MockPrompt.from_template.return_value
        mock_intermediate = MagicMock()
        mock_chain = MagicMock()

        mock_prompt_instance.__or__.return_value = mock_intermediate
        mock_intermediate.__or__.return_value = mock_chain

        mock_chain.invoke.return_value = "Quotes"

        result = agent.generate_quotes("Details", "Person", "Company")
        assert result == "Quotes"

def test_adapt_audience():
    with patch('agent.core.Config') as MockConfig, \
         patch('agent.core.ChatOpenAI'), \
         patch('agent.core.ChatPromptTemplate') as MockPrompt:

        MockConfig.DEFAULT_MODEL_PROVIDER = 'openai'
        MockConfig.OPENAI_API_KEY = 'test'

        agent = PressReleaseGenerator()

        mock_prompt_instance = MockPrompt.from_template.return_value
        mock_intermediate = MagicMock()
        mock_chain = MagicMock()

        mock_prompt_instance.__or__.return_value = mock_intermediate
        mock_intermediate.__or__.return_value = mock_chain

        mock_chain.invoke.return_value = "Adapted Text"

        result = agent.adapt_audience("Lead", "Audience")
        assert result == "Adapted Text"
