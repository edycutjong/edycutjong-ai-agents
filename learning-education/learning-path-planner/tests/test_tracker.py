import sys
import os
import pytest
import json

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.tracker import ProgressTracker
from agent.models import LearningPath, Milestone, Resource, Project

@pytest.fixture
def temp_tracker(tmp_path):
    file = tmp_path / "test_path.json"
    return ProgressTracker(str(file))

def test_save_load_path(temp_tracker):
    path = LearningPath(
        topic="Test",
        user_level="Beginner",
        total_estimated_time="1 week",
        milestones=[
            Milestone(
                id=1,
                title="M1",
                description="D1",
                skills=["S1"],
                resources=[],
                estimated_time="1d",
                is_completed=False,
                projects=[]
            )
        ]
    )
    temp_tracker.save_path(path)
    loaded_path = temp_tracker.load_path()
    assert loaded_path is not None
    assert loaded_path.topic == "Test"
    assert len(loaded_path.milestones) == 1

def test_mark_complete(temp_tracker):
    path = LearningPath(
        topic="Test",
        user_level="Beginner",
        total_estimated_time="1 week",
        milestones=[
            Milestone(
                id=1,
                title="M1",
                description="D1",
                skills=["S1"],
                resources=[],
                estimated_time="1d",
                is_completed=False,
                projects=[]
            )
        ]
    )
    temp_tracker.save_path(path)
    updated_path = temp_tracker.mark_milestone_complete(1)
    assert updated_path.milestones[0].is_completed is True

    loaded_path = temp_tracker.load_path()
    assert loaded_path.milestones[0].is_completed is True
