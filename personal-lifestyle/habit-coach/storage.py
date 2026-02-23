import json
import os
from datetime import date, datetime
from typing import List, Optional
try:
    from .models import Habit, HabitLog
except ImportError:
    from models import Habit, HabitLog

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
HABITS_FILE = os.path.join(DATA_DIR, "habits.json")
LOGS_FILE = os.path.join(DATA_DIR, "logs.json")

def _ensure_data_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(HABITS_FILE):
        with open(HABITS_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, "w") as f:
            json.dump([], f)

def _load_habits() -> List[Habit]:
    _ensure_data_files()
    with open(HABITS_FILE, "r") as f:
        data = json.load(f)
    return [Habit(**item) for item in data]

def _save_habits(habits: List[Habit]):
    _ensure_data_files()
    with open(HABITS_FILE, "w") as f:
        json.dump([h.model_dump(mode='json') for h in habits], f, indent=2)

def _load_logs() -> List[HabitLog]:
    _ensure_data_files()
    with open(LOGS_FILE, "r") as f:
        data = json.load(f)
    return [HabitLog(**item) for item in data]

def _save_logs(logs: List[HabitLog]):
    _ensure_data_files()
    with open(LOGS_FILE, "w") as f:
        json.dump([l.model_dump(mode='json') for l in logs], f, indent=2)

# --- Public API ---

def add_habit(name: str, description: Optional[str] = None, frequency: str = "daily") -> Habit:
    habits = _load_habits()
    new_habit = Habit(name=name, description=description, frequency=frequency)
    habits.append(new_habit)
    _save_habits(habits)
    return new_habit

def get_habits() -> List[Habit]:
    return _load_habits()

def get_habit_by_name(name: str) -> Optional[Habit]:
    habits = _load_habits()
    for h in habits:
        if h.name.lower() == name.lower():
            return h
    return None

def delete_habit(habit_id: str):
    habits = _load_habits()
    habits = [h for h in habits if h.id != habit_id]
    _save_habits(habits)
    # Also remove associated logs? Maybe keep them for history.
    # For now, let's keep them but maybe filter them out in analytics if habit doesn't exist.

def log_habit(habit_id: str, log_date: date, status: str = "completed", notes: Optional[str] = None) -> HabitLog:
    logs = _load_logs()
    # Check if already logged for this date
    existing_log = next((l for l in logs if l.habit_id == habit_id and l.date == log_date), None)

    if existing_log:
        existing_log.status = status
        existing_log.notes = notes
        _save_logs(logs)
        return existing_log

    new_log = HabitLog(date=log_date, habit_id=habit_id, status=status, notes=notes)
    logs.append(new_log)
    _save_logs(logs)
    return new_log

def get_logs(habit_id: Optional[str] = None) -> List[HabitLog]:
    logs = _load_logs()
    if habit_id:
        return [l for l in logs if l.habit_id == habit_id]
    return logs
