import pytest
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

@pytest.fixture
def sample_article():
    return {
        "title": "New AI Model Released",
        "link": "https://example.com/ai-model",
        "published": "2023-10-27 10:00:00",
        "summary": "A new AI model has been released by TechCorp.",
        "source": "TechNews"
    }

@pytest.fixture
def sample_processed_article():
    return {
        "title": "New AI Model Released",
        "link": "https://example.com/ai-model",
        "published": "2023-10-27 10:00:00",
        "summary": "Detailed summary of the AI model.",
        "source": "TechNews",
        "relevant": True,
        "category": "Artificial Intelligence",
        "score": 9
    }
