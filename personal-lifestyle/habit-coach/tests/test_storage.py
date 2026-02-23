import pytest
import os
import json
from datetime import date
from models import Habit
from storage import add_habit, get_habits, log_habit, get_logs, delete_habit, _ensure_data_files

# Setup fixture to use a temporary data directory or clear files
@pytest.fixture(autouse=True)
def setup_teardown():
    # Store original paths
    original_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    habits_file = os.path.join(original_data_dir, "habits.json")
    logs_file = os.path.join(original_data_dir, "logs.json")

    # Backup existing data
    backup_habits = []
    backup_logs = []
    if os.path.exists(habits_file):
        with open(habits_file, 'r') as f:
            backup_habits = json.load(f)
    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            backup_logs = json.load(f)

    # Clear data for test
    with open(habits_file, 'w') as f:
        json.dump([], f)
    with open(logs_file, 'w') as f:
        json.dump([], f)

    yield

    # Restore data
    with open(habits_file, 'w') as f:
        json.dump(backup_habits, f)
    with open(logs_file, 'w') as f:
        json.dump(backup_logs, f)

def test_add_habit():
    h = add_habit("Test Habit", "Description")
    habits = get_habits()
    assert len(habits) == 1
    assert habits[0].name == "Test Habit"
    assert habits[0].id == h.id

def test_log_habit():
    h = add_habit("Test Habit")
    today = date.today()
    log = log_habit(h.id, today, "completed")

    logs = get_logs(h.id)
    assert len(logs) == 1
    assert logs[0].status == "completed"
    assert logs[0].date == today

def test_delete_habit():
    h = add_habit("Test Habit")
    assert len(get_habits()) == 1
    delete_habit(h.id)
    assert len(get_habits()) == 0
