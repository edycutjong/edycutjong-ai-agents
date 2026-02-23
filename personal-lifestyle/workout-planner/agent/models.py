from typing import List, Optional
from pydantic import BaseModel, Field

class Exercise(BaseModel):
    name: str = Field(..., description="Name of the exercise")
    sets: Optional[str] = Field(None, description="Number of sets (e.g., '3', '3-4')")
    reps: Optional[str] = Field(None, description="Number of repetitions (e.g., '10', '12-15')")
    duration: Optional[str] = Field(None, description="Duration if applicable (e.g., '30 seconds', '5 mins')")
    notes: Optional[str] = Field(None, description="Technique notes or rest instructions")

class WorkoutSession(BaseModel):
    day: str = Field(..., description="Day of the week (e.g., 'Monday')")
    workout_type: str = Field(..., description="Type of workout (e.g., 'Full Body', 'HIIT', 'Rest')")
    warm_up: List[str] = Field(..., description="List of warm-up activities")
    main_workout: List[Exercise] = Field(..., description="List of exercises for the main workout")
    cool_down: List[str] = Field(..., description="List of cool-down activities")
    duration_minutes: int = Field(..., description="Estimated total duration in minutes")
    estimated_calories: int = Field(..., description="Estimated calories burned")

class WeeklyPlan(BaseModel):
    week_number: int = Field(..., description="Week number in the program")
    focus: str = Field(..., description="Main focus for this week")
    sessions: List[WorkoutSession] = Field(..., description="List of daily workout sessions")

class WorkoutPlan(BaseModel):
    plan_name: str = Field(..., description="Name of the workout plan")
    weeks: List[WeeklyPlan] = Field(..., description="List of weekly plans")
    difficulty_progression: str = Field(..., description="Explanation of how difficulty progresses over the weeks")
    equipment_needed: List[str] = Field(..., description="List of equipment required for this plan")

class UserProfile(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    fitness_goal: str
    fitness_level: str
    equipment: List[str]
    days_per_week: int
    duration_per_session: int
