import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_weekly_plan():
    from agent.models import WeeklyPlan, DailyPlan, Recipe, Ingredient, NutritionInfo

    ingredient = Ingredient(name="Egg", quantity=2, unit="large")
    nutrition = NutritionInfo(calories=150, protein_g=12, carbs_g=1, fat_g=10)
    recipe = Recipe(
        name="Boiled Eggs",
        ingredients=[ingredient],
        instructions=["Boil water", "Add eggs", "Cook 10 mins"],
        nutrition=nutrition,
        estimated_cost=0.50,
        prep_time_minutes=12
    )

    daily_plan = DailyPlan(
        day=1,
        breakfast=recipe,
        lunch=recipe,
        dinner=recipe,
        snacks=[recipe]
    )

    return WeeklyPlan(
        daily_plans=[daily_plan],
        meal_prep_tips=["Boil eggs in advance"],
        total_estimated_cost=10.0
    )

@pytest.fixture
def mock_shopping_list():
    from agent.models import ShoppingList, ShoppingItem
    item = ShoppingItem(name="Egg", quantity=10, unit="large", category="Dairy")
    return ShoppingList(items=[item])
