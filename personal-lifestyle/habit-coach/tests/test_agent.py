import pytest
from unittest.mock import MagicMock, patch
from agent.tools import add_new_habit, log_completion, get_habit_stats, get_habit_list
from models import Habit
from storage import add_habit, log_habit, delete_habit, _ensure_data_files
from datetime import date
import os
import json

@pytest.fixture(autouse=True)
def setup_teardown():
    original_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    habits_file = os.path.join(original_data_dir, "habits.json")
    logs_file = os.path.join(original_data_dir, "logs.json")

    backup_habits = []
    backup_logs = []
    if os.path.exists(habits_file):
        with open(habits_file, 'r') as f:
            backup_habits = json.load(f)
    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            backup_logs = json.load(f)

    with open(habits_file, 'w') as f:
        json.dump([], f)
    with open(logs_file, 'w') as f:
        json.dump([], f)

    yield

    with open(habits_file, 'w') as f:
        json.dump(backup_habits, f)
    with open(logs_file, 'w') as f:
        json.dump(backup_logs, f)

def test_add_new_habit_tool():
    result = add_new_habit.invoke({"name": "Test Tool Habit", "description": "From Tool"})
    assert "Added habit: Test Tool Habit" in result

    habits = get_habit_list.invoke({})
    assert "Test Tool Habit" in habits

def test_log_completion_tool():
    add_habit("Log Tool Habit")
    result = log_completion.invoke({"habit_name": "Log Tool Habit", "status": "completed"})
    assert "Logged 'Log Tool Habit' as completed" in result

def test_get_habit_stats_tool():
    add_habit("Stats Habit")
    log_completion.invoke({"habit_name": "Stats Habit", "status": "completed"})

    stats = get_habit_stats.invoke({"habit_name": "Stats Habit"})
    assert "Current Streak: 1 days" in stats
