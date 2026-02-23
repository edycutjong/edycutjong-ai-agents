from langchain_openai import ChatOpenAI
from agent.models import WorkoutPlan, UserProfile
from prompts.workout_prompts import get_workout_prompt
from config import OPENAI_API_KEY, MODEL_NAME

def generate_workout_plan(user_profile: UserProfile, model_name: str = MODEL_NAME) -> WorkoutPlan:
    """
    Generates a personalized workout plan using the specified LLM.
    """

    # Check for API key
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    llm = ChatOpenAI(model=model_name, temperature=0.7)
    structured_llm = llm.with_structured_output(WorkoutPlan)
    prompt = get_workout_prompt()
    chain = prompt | structured_llm

    # Format equipment list
    equipment_str = ", ".join(user_profile.equipment) if user_profile.equipment else "Bodyweight only"

    return chain.invoke({
        "name": user_profile.name,
        "age": user_profile.age,
        "gender": "Not specified",
        "weight": user_profile.weight,
        "height": user_profile.height,
        "fitness_goal": user_profile.fitness_goal,
        "fitness_level": user_profile.fitness_level,
        "equipment": equipment_str,
        "days_per_week": user_profile.days_per_week,
        "duration_per_session": user_profile.duration_per_session
    })
