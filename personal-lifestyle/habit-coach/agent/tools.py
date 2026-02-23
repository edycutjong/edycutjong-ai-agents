from langchain.tools import tool
from typing import Optional, List
from datetime import date
try:
    from ..storage import add_habit, get_habits, log_habit, get_logs
    from ..analytics import calculate_current_streak, calculate_completion_rate, get_best_day_of_week
except ImportError:
    # For relative import issues during standalone run, try absolute if possible or fix path
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from storage import add_habit, get_habits, log_habit, get_logs
    from analytics import calculate_current_streak, calculate_completion_rate, get_best_day_of_week

@tool
def add_new_habit(name: str, description: Optional[str] = None, frequency: str = "daily") -> str:
    """Adds a new habit to track. Returns the confirmation message."""
    habit = add_habit(name, description, frequency)
    return f"Added habit: {habit.name} (ID: {habit.id})"

@tool
def log_completion(habit_name: str, status: str = "completed", notes: Optional[str] = None) -> str:
    """Logs a completion for a habit by name for today. Status can be 'completed' or 'skipped'."""
    habits = get_habits()
    habit = next((h for h in habits if h.name.lower() == habit_name.lower()), None)
    if not habit:
        return f"Habit '{habit_name}' not found."

    log = log_habit(habit.id, date.today(), status, notes)
    return f"Logged '{habit.name}' as {status} for today ({log.date})."

@tool
def get_habit_list() -> str:
    """Returns a list of all tracked habits."""
    habits = get_habits()
    if not habits:
        return "No habits found."
    return "\n".join([f"- {h.name}: {h.description or 'No description'} ({h.frequency})" for h in habits])

@tool
def get_habit_stats(habit_name: str) -> str:
    """Returns statistics for a specific habit (streak, completion rate, best day)."""
    habits = get_habits()
    habit = next((h for h in habits if h.name.lower() == habit_name.lower()), None)
    if not habit:
        return f"Habit '{habit_name}' not found."

    streak = calculate_current_streak(habit.id)
    rate = calculate_completion_rate(habit.id)
    best_day = get_best_day_of_week(habit.id)

    return (f"Stats for {habit.name}:\n"
            f"- Current Streak: {streak} days\n"
            f"- 30-day Completion Rate: {rate:.1f}%\n"
            f"- Best Performance Day: {best_day}")
