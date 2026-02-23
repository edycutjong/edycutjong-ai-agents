import pytest
import os
import sys

# Ensure config is importable
sys.path.append(os.path.join(os.getcwd(), 'apps/agents/design-frontend/ui-copy-reviewer'))

from agent.reviewer import ReviewerAgent
import config

class TestReviewer:
    @pytest.fixture
    def mock_agent(self):
        # Force mock LLM
        original_use_mock = config.USE_MOCK_LLM
        config.USE_MOCK_LLM = True

        agent = ReviewerAgent()

        yield agent

        config.USE_MOCK_LLM = original_use_mock

    def test_review_text_mocked(self, mock_agent):
        # The FakeListLLM in ReviewerAgent returns a sequence of responses.
        # We need to know what to expect.
        # Responses: "OK", "Suggestion...", "Flag...", "OK", "Suggestion...", "Tone..."

        # Test 1: Inclusive Language -> "OK"
        # Test 2: Consistency -> "Suggestion..."
        # ...

        # Let's just run review_text and see what we get.
        # Since it iterates over keys in a dict, order might vary in older Python,
        # but 3.7+ preserves insertion order.
        # Checks: Inclusive, Consistency, Jargon, Localizability, Clarity, Voice

        # Expected from FakeListLLM in _get_llm:
        # 1. OK (Inclusive)
        # 2. Suggestion... (Consistency) -> Issue!
        # 3. Flag... (Jargon) -> Issue!
        # 4. OK (Localizability)
        # 5. Suggestion... (Clarity) -> Issue!
        # 6. Tone... (Voice) -> Issue!

        results = mock_agent.review_text("Test string")

        assert "Inclusive Language" not in results
        assert "Consistency" in results
        assert "Jargon" in results
        assert "Localizability" not in results
        assert "Clarity" in results
        assert "Voice & Tone" in results

    def test_review_items(self, mock_agent):
        items = [{'text': 'Sign In', 'context': '<button>Sign In</button>'}]

        # Since FakeListLLM cycles, the next call will continue the sequence.
        # Previous test consumed 6 responses.
        # Sequence length is 6. So we are back to start.

        reviewed = mock_agent.review_items(items)

        assert len(reviewed) == 1
        issues = reviewed[0]['issues']
        assert "Consistency" in issues
        assert "Jargon" in issues
        # ... based on the same sequence

    def test_skip_short_text(self, mock_agent):
        items = [{'text': 'OK'}, {'text': '12'}]
        reviewed = mock_agent.review_items(items)
        assert len(reviewed) == 0
