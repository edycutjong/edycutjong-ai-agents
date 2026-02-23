import sys
import os
import pytest
from pydantic import ValidationError

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.planner import LearningPathPlanner
from agent.models import LearningPath
from config import config

@pytest.fixture
def planner():
    config.MOCK_MODE = True
    return LearningPathPlanner()

def test_generate_path(planner):
    path = planner.generate_path("Python", "Beginner")
    assert isinstance(path, LearningPath)
    assert path.topic == "Python"
    assert path.user_level == "Beginner"
    assert len(path.milestones) > 0

def test_adjust_path(planner):
    path = planner.generate_path("Python", "Beginner")
    updated_path = planner.adjust_path(path, "I finished the first milestone.")
    assert isinstance(updated_path, LearningPath)
    # Mock adjustment doesn't change much but returns a valid path
    assert updated_path.topic == path.topic
