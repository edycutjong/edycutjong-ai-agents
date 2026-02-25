import pytest
from datetime import date, timedelta
from analytics import calculate_current_streak, calculate_longest_streak, calculate_completion_rate, get_best_day_of_week
from storage import add_habit, log_habit, delete_habit, _ensure_data_files, get_logs
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

def test_optimized_analytics_pass_logs():
    h = add_habit("Optimized Habit")
    today = date.today()

    # Add some logs
    log_habit(h.id, today, "completed")
    log_habit(h.id, today - timedelta(days=1), "completed")
    log_habit(h.id, today - timedelta(days=3), "completed")

    logs = get_logs(h.id)
    assert len(logs) == 3

    # Test with logs passed explicitly
    assert calculate_current_streak(h.id, logs=logs) == 2
    assert calculate_longest_streak(h.id, logs=logs) == 2

    # For completion rate, we have 3 logs in last 30 days
    # 3 / 30 * 100 = 10.0
    assert calculate_completion_rate(h.id, logs=logs) == 10.0

    # Best day depends on today's weekday.
    assert isinstance(get_best_day_of_week(h.id, logs=logs), str)

def test_get_all_habits_summary_uses_optimization():
    h1 = add_habit("Habit 1")
    h2 = add_habit("Habit 2")

    log_habit(h1.id, date.today(), "completed")
    log_habit(h2.id, date.today(), "completed")

    from analytics import get_all_habits_summary
    summary = get_all_habits_summary()
    assert len(summary) == 2

    # Find summary for h1 and h2
    s1 = next(s for s in summary if s["id"] == h1.id)
    s2 = next(s for s in summary if s["id"] == h2.id)

    assert s1["current_streak"] == 1
    assert s2["current_streak"] == 1
