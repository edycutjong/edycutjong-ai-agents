import sys
import os

# Add the parent directory (project root) to sys.path to allow importing 'agent'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.models import Exercise, WorkoutSession, WeeklyPlan, WorkoutPlan, UserProfile

def test_exercise_creation():
    ex = Exercise(name="Pushups", sets="3", reps="10", notes="Keep back straight")
    assert ex.name == "Pushups"
    assert ex.sets == "3"
    assert ex.reps == "10"

def test_workout_session_creation():
    ex = Exercise(name="Pushups", sets="3", reps="10")
    session = WorkoutSession(
        day="Monday",
        workout_type="Strength",
        warm_up=["Jogging", "Arm circles"],
        main_workout=[ex],
        cool_down=["Stretching"],
        duration_minutes=45,
        estimated_calories=300
    )
    assert session.day == "Monday"
    assert len(session.main_workout) == 1
    assert session.estimated_calories == 300

def test_weekly_plan_creation():
    ex = Exercise(name="Pushups", sets="3", reps="10")
    session = WorkoutSession(
        day="Monday",
        workout_type="Strength",
        warm_up=["Jogging"],
        main_workout=[ex],
        cool_down=["Stretching"],
        duration_minutes=45,
        estimated_calories=300
    )
    plan = WeeklyPlan(week_number=1, focus="Full Body", sessions=[session])
    assert plan.week_number == 1
    assert len(plan.sessions) == 1

def test_workout_plan_creation():
    # Setup dependencies
    ex = Exercise(name="Squats", sets="3", reps="12")
    session = WorkoutSession(
        day="Monday",
        workout_type="Legs",
        warm_up=["Jump rope"],
        main_workout=[ex],
        cool_down=["Stretch"],
        duration_minutes=30,
        estimated_calories=200
    )
    weekly = WeeklyPlan(week_number=1, focus="Legs", sessions=[session])

    plan = WorkoutPlan(
        plan_name="Leg Blaster",
        weeks=[weekly],
        difficulty_progression="Increase weight by 5%",
        equipment_needed=["Dumbbells"]
    )
    assert plan.plan_name == "Leg Blaster"
    assert len(plan.weeks) == 1

def test_user_profile_creation():
    user = UserProfile(
        name="John Doe",
        age=30,
        weight=80.0,
        height=180.0,
        fitness_goal="Muscle Gain",
        fitness_level="Intermediate",
        equipment=["Dumbbells", "Bench"],
        days_per_week=4,
        duration_per_session=60
    )
    assert user.name == "John Doe"
    assert user.age == 30
