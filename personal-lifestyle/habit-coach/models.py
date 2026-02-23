from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
import uuid

class Habit(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    frequency: str = "daily"  # daily, weekly
    created_at: datetime = Field(default_factory=datetime.now)

class HabitLog(BaseModel):
    date: date
    habit_id: str
    status: str = "completed"  # completed, skipped
    notes: Optional[str] = None
