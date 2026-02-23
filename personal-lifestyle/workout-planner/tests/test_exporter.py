import sys
import os
import pytest

# Fix path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.models import WorkoutPlan, WeeklyPlan, WorkoutSession, Exercise
from agent.exporter import export_to_markdown, export_to_pdf

def test_export_to_markdown(tmp_path):
    ex = Exercise(name="Pushups", sets="3", reps="10")
    session = WorkoutSession(
        day="Monday", workout_type="Strength", warm_up=["Jog"],
        main_workout=[ex], cool_down=["Stretch"],
        duration_minutes=30, estimated_calories=200
    )
    week = WeeklyPlan(week_number=1, focus="Intro", sessions=[session])
    plan = WorkoutPlan(
        plan_name="Test Plan", weeks=[week],
        difficulty_progression="None", equipment_needed=["None"]
    )

    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test.md"
    export_to_markdown(plan, str(p))
    content = p.read_text()
    assert content.startswith("# Test Plan")
    assert "Pushups" in content

def test_export_to_pdf(tmp_path):
    ex = Exercise(name="Pushups", sets="3", reps="10")
    session = WorkoutSession(
        day="Monday", workout_type="Strength", warm_up=["Jog"],
        main_workout=[ex], cool_down=["Stretch"],
        duration_minutes=30, estimated_calories=200
    )
    week = WeeklyPlan(week_number=1, focus="Intro", sessions=[session])
    plan = WorkoutPlan(
        plan_name="Test Plan", weeks=[week],
        difficulty_progression="None", equipment_needed=["None"]
    )

    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test.pdf"
    export_to_pdf(plan, str(p))
    assert p.exists()
    assert p.stat().st_size > 0
