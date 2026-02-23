import pytest
from unittest.mock import MagicMock, patch
import json
import os
from agent.gift_advisor import GiftAdvisor, GiftSuggestion
from langchain_core.messages import AIMessage

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        yield

@pytest.fixture
def mock_llm_class():
    with patch("agent.gift_advisor.ChatOpenAI") as mock:
        yield mock

@pytest.fixture
def mock_search_tool():
    with patch("agent.gift_advisor.SearchTool") as mock:
        yield mock

@pytest.fixture
def advisor(mock_llm_class, mock_search_tool, tmp_path):
    # Mock os.makedirs to avoid creating directories in real fs (though tmp_path handles it usually)
    with patch("os.makedirs"):
        advisor = GiftAdvisor(api_key="test_key")
        # Redirect history file to tmp_path
        advisor.history_file = str(tmp_path / "history.json")
        return advisor

def test_initialization(advisor):
    assert advisor.llm is not None
    assert advisor.history_file.endswith("history.json")

def test_generate_suggestions(advisor):
    # We need to mock the chain execution.
    # Since `chain = prompt | llm | parser`, it's hard to mock the intermediate steps easily without deep knowledge of LangChain internals.
    # Instead, we can mock the `invoke` method if we can intercept the chain construction.
    # But we can't easily.

    # Alternative: Mock ChatOpenAI to behave like a Runnable that returns a valid message.
    # And ensure JsonOutputParser works.

    # However, `ChatOpenAI` is mocked. `mock_llm_class.return_value` is the instance `self.llm`.
    # When `prompt | self.llm` happens, `ChatPromptTemplate`'s `__or__` is called with `self.llm`.
    # If `self.llm` is a MagicMock, `__or__` might fail or return something unexpected depending on MagicMock config.
    # LangChain's `__or__` checks if right side is Runnable. MagicMock isn't by default.

    # Strategy: Patch `agent.gift_advisor.ChatPromptTemplate` so that `from_messages` returns a mock object.
    # This mock object's `__or__` (pipe) should return another mock (the chain), whose `invoke` returns the desired dict.

    expected_result = {
        "gifts": [
            {
                "name": "Test Gift",
                "category": "Tech",
                "reasoning": "Because it's cool",
                "estimated_price": "$100",
                "search_query": "buy test gift"
            }
        ]
    }

    with patch("agent.gift_advisor.ChatPromptTemplate") as MockPrompt:
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = expected_result

        # Setup the chain of pipes to return mock_chain eventually
        # prompt | llm | parser -> mock_chain
        # We can just make the prompt mock return mock_chain when piped.
        mock_prompt_instance = MockPrompt.from_messages.return_value

        # prompt | llm -> intermediate
        # intermediate | parser -> chain

        mock_intermediate = MagicMock()
        mock_prompt_instance.__or__.return_value = mock_intermediate
        mock_intermediate.__or__.return_value = mock_chain

        # Call the method
        suggestions = advisor.generate_suggestions(
            profile={"name": "Alice"},
            occasion="Birthday",
            budget="$100"
        )

        assert len(suggestions) == 1
        assert suggestions[0].name == "Test Gift"
        assert suggestions[0].reasoning == "Because it's cool"
        # Check if history was saved (file created)
        assert os.path.exists(advisor.history_file)
        with open(advisor.history_file, 'r') as f:
            history = json.load(f)
            assert len(history) == 1
            assert history[0]['profile']['name'] == "Alice"

def test_save_load_history(advisor):
    profile = {"name": "Bob"}
    suggestions = [
        GiftSuggestion(
            name="Book",
            category="Read",
            reasoning="Good book",
            estimated_price="$20",
            search_query="book",
            purchase_link="http://book"
        )
    ]

    advisor.save_history(profile, "Holiday", suggestions)

    loaded = advisor.load_history()
    assert len(loaded) == 1
    assert loaded[0]['profile']['name'] == "Bob"
    assert loaded[0]['suggestions'][0]['name'] == "Book"

def test_search_fallback(advisor):
    # Test that if search tool fails, we still get a fallback link
    with patch("agent.gift_advisor.ChatPromptTemplate") as MockPrompt:
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "gifts": [{"name": "G", "category": "C", "reasoning": "R", "estimated_price": "P", "search_query": "Q"}]
        }
        mock_prompt_instance = MockPrompt.from_messages.return_value
        mock_prompt_instance.__or__.return_value.__or__.return_value = mock_chain

        # Mock search tool to raise exception
        advisor.search_tool.search_gift_links.side_effect = Exception("Search failed")

        suggestions = advisor.generate_suggestions({}, "Occasion", "Budget")

        assert len(suggestions) == 1
        assert suggestions[0].purchase_link.startswith("https://www.google.com/search")
