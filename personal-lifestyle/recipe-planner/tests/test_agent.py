import pytest
from unittest.mock import MagicMock, patch
from agent.planner import RecipePlannerAgent
from agent.models import WeeklyPlan, ShoppingList, Recipe, Ingredient, NutritionInfo, DailyPlan

def test_generate_plan(mock_weekly_plan):
    with patch("agent.planner.ChatOpenAI") as MockChat:
        # Mock the llm instance
        mock_llm = MagicMock()
        MockChat.return_value = mock_llm

        # Mock the invoke response
        mock_response = MagicMock()
        mock_response.content = mock_weekly_plan.model_dump_json()
        mock_llm.invoke.return_value = mock_response

        agent = RecipePlannerAgent()
        plan = agent.generate_plan("Vegan", "None", "Low", 3)

        assert isinstance(plan, WeeklyPlan)
        assert len(plan.daily_plans) == 1
        assert plan.total_estimated_cost == 10.0
        assert plan.daily_plans[0].breakfast.name == "Boiled Eggs"

def test_generate_shopping_list(mock_weekly_plan, mock_shopping_list):
    with patch("agent.planner.ChatOpenAI") as MockChat:
        mock_llm = MagicMock()
        MockChat.return_value = mock_llm

        mock_response = MagicMock()
        mock_response.content = mock_shopping_list.model_dump_json()
        mock_llm.invoke.return_value = mock_response

        agent = RecipePlannerAgent()
        shopping_list = agent.generate_shopping_list(mock_weekly_plan)

        assert isinstance(shopping_list, ShoppingList)
        assert len(shopping_list.items) == 1
        assert shopping_list.items[0].name == "Egg"

def test_format_to_markdown(mock_weekly_plan, mock_shopping_list):
    agent = RecipePlannerAgent(api_key="dummy")
    md = agent.format_to_markdown(mock_weekly_plan, mock_shopping_list)

    assert "# 🥗 Weekly Meal Plan" in md
    assert "**Total Estimated Cost:** $10.00" in md
    assert "### Day 1" in md
    assert "#### 🍳 Breakfast: Boiled Eggs" in md
    assert "## 🛒 Shopping List" in md
    assert "### Dairy" in md
    assert "- Egg: 10.0 large" in md
    assert "## 🔪 Meal Prep Strategies" in md
    assert "- Boil eggs in advance" in md
