import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.evaluator import RAGEvaluator

def test_evaluator_mock():
    print("Initializing Evaluator with mock key...")
    # Initialize with a dummy key
    evaluator = RAGEvaluator(openai_api_key="sk-mock-key")

    # Mock the LLM to return a predictable score
    evaluator.llm = MagicMock()
    evaluator.llm.invoke.return_value.content = "0.95" # Simulate LLM returning a high score

    # Patch the chain invocation inside _get_score because we are mocking the chain construction
    # But wait, _get_score constructs the chain: chain = prompt | self.llm | StrOutputParser()
    # So we need to ensure that pipeline executes.

    # Easier way: Mock _get_score to return fixed values to verify the `evaluate` method orchestrates them correctly.
    # OR Mock ChatOpenAI response.

    with patch('agent.evaluator.ChatOpenAI') as MockLLM:
        # We need to simulate the chain execution result.
        # Since _get_score does: prompt | llm | StrOutputParser()
        # We can mock `invoke` on the result of the pipe.

        # Actually, let's just mock _get_score for unit testing `evaluate` aggregation
        # and test _get_score logic separately if possible.

        # Let's try mocking the LLM call directly.
        pass

    # Let's just create a new instance where we mock _get_score
    evaluator._get_score = MagicMock(return_value=0.9)

    scores = evaluator.evaluate(
        question="What is RAG?",
        answer="RAG stands for Retrieval Augmented Generation.",
        context="RAG is a technique..."
    )

    print(f"Scores: {scores}")
    assert scores["faithfulness"] == 0.9
    assert scores["answer_relevance"] == 0.9
    assert scores["context_precision"] == 0.9

if __name__ == "__main__":
    test_evaluator_mock()
