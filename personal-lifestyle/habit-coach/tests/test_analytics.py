import pytest
from datetime import date, timedelta
from analytics import calculate_current_streak, calculate_longest_streak, calculate_completion_rate, get_best_day_of_week
from storage import add_habit, log_habit, delete_habit, _ensure_data_files
from models import Habit
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

def test_streak_calculation():
    h = add_habit("Streak Habit")
    today = date.today()

    # No logs
    assert calculate_current_streak(h.id) == 0

    # Log today
    log_habit(h.id, today, "completed")
    assert calculate_current_streak(h.id) == 1

    # Log yesterday
    log_habit(h.id, today - timedelta(days=1), "completed")
    assert calculate_current_streak(h.id) == 2

    # Gap
    log_habit(h.id, today - timedelta(days=3), "completed")
    assert calculate_current_streak(h.id) == 2 # Still 2
    assert calculate_longest_streak(h.id) == 2

def test_completion_rate():
    h = add_habit("Rate Habit")
    today = date.today()

    # Log 15 days out of last 30
    for i in range(15):
        log_habit(h.id, today - timedelta(days=i*2), "completed") # Every other day

    rate = calculate_completion_rate(h.id, days=30)
    assert rate == 50.0

def test_best_day():
    h = add_habit("Day Habit")
    # Log 3 Mondays and 1 Tuesday
    # Find a Monday
    today = date.today()
    monday_offset = today.weekday() # 0 is Monday
    last_monday = today - timedelta(days=monday_offset)

    for i in range(3):
        d = last_monday - timedelta(weeks=i)
        log_habit(h.id, d, "completed")

    log_habit(h.id, last_monday + timedelta(days=1), "completed") # A Tuesday

    assert get_best_day_of_week(h.id) == "Monday"
