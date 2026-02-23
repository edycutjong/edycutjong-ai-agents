from datetime import date, timedelta
from typing import List, Dict, Any
from collections import Counter
import pandas as pd
try:
    from .storage import get_logs, get_habits
except ImportError:
    from storage import get_logs, get_habits

def calculate_current_streak(habit_id: str) -> int:
    logs = get_logs(habit_id)
    # Filter only completed
    completed_dates = sorted([l.date for l in logs if l.status == 'completed'], reverse=True)

    if not completed_dates:
        return 0

    today = date.today()
    streak = 0

    # Check if completed today or yesterday to start the streak
    if completed_dates[0] == today:
        current_check = today
    elif completed_dates[0] == today - timedelta(days=1):
        current_check = today - timedelta(days=1)
    else:
        return 0 # Streak broken

    for d in completed_dates:
        if d == current_check:
            streak += 1
            current_check -= timedelta(days=1)
        elif d > current_check:
            continue # Duplicate log for same day?
        else:
            break # Gap found

    return streak

def calculate_longest_streak(habit_id: str) -> int:
    logs = get_logs(habit_id)
    completed_dates = sorted(list(set([l.date for l in logs if l.status == 'completed'])))

    if not completed_dates:
        return 0

    longest_streak = 0
    current_streak = 0
    last_date = None

    for d in completed_dates:
        if last_date is None:
            current_streak = 1
        elif d == last_date + timedelta(days=1):
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
        last_date = d

    longest_streak = max(longest_streak, current_streak)
    return longest_streak

def calculate_completion_rate(habit_id: str, days: int = 30) -> float:
    logs = get_logs(habit_id)
    cutoff_date = date.today() - timedelta(days=days)
    relevant_logs = [l for l in logs if l.date >= cutoff_date and l.status == 'completed']

    # Simple calculation: completions / days.
    # Note: This assumes daily habit. For weekly it's different.
    # For now, let's just do count / days * 100

    return (len(relevant_logs) / days) * 100

def get_best_day_of_week(habit_id: str) -> str:
    logs = get_logs(habit_id)
    completed_dates = [l.date for l in logs if l.status == 'completed']

    if not completed_dates:
        return "N/A"

    weekdays = [d.strftime("%A") for d in completed_dates]
    count = Counter(weekdays)
    return count.most_common(1)[0][0]

def get_all_habits_summary() -> List[Dict[str, Any]]:
    habits = get_habits()
    summary = []
    for h in habits:
        summary.append({
            "id": h.id,
            "name": h.name,
            "current_streak": calculate_current_streak(h.id),
            "longest_streak": calculate_longest_streak(h.id),
            "completion_rate_30d": calculate_completion_rate(h.id),
            "best_day": get_best_day_of_week(h.id)
        })
    return summary
