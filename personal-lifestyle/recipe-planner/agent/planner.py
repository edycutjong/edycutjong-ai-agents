from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .models import WeeklyPlan, ShoppingList, Recipe, DailyPlan, Ingredient

class RecipePlannerAgent:
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None):
        self.llm = ChatOpenAI(model=model_name, api_key=api_key)
        self.weekly_parser = PydanticOutputParser(pydantic_object=WeeklyPlan)
        self.shopping_parser = PydanticOutputParser(pydantic_object=ShoppingList)

    def generate_plan(self, preferences: str, allergies: str, budget: str, days: int) -> WeeklyPlan:
        template = """
        You are a professional Nutritionist and Meal Planner.
        Your goal is to create a healthy, cost-effective, and delicious meal plan.

        User Preferences:
        - Dietary Preferences: {preferences}
        - Allergies/Restrictions: {allergies}
        - Budget Level: {budget}
        - Number of Days: {days}

        Please generate a structured weekly meal plan following these constraints.
        Include detailed recipes, nutritional info, and estimated costs.
        Also provide meal prep strategies.

        {format_instructions}
        """

        prompt = ChatPromptTemplate.from_template(template)

        messages = prompt.format_messages(
            preferences=preferences,
            allergies=allergies,
            budget=budget,
            days=days,
            format_instructions=self.weekly_parser.get_format_instructions()
        )

        response = self.llm.invoke(messages)
        return self.weekly_parser.parse(response.content)

    def generate_shopping_list(self, plan: WeeklyPlan) -> ShoppingList:
        template = """
        You are a helpful assistant that generates a consolidated shopping list from a meal plan.
        Group items by category (Produce, Dairy, Meat, Pantry, etc.).
        Sum up quantities of the same ingredient.

        Here is the meal plan:
        {plan_json}

        {format_instructions}
        """

        prompt = ChatPromptTemplate.from_template(template)

        # Convert plan to JSON string for the prompt
        plan_json = plan.model_dump_json()

        messages = prompt.format_messages(
            plan_json=plan_json,
            format_instructions=self.shopping_parser.get_format_instructions()
        )

        response = self.llm.invoke(messages)
        return self.shopping_parser.parse(response.content)

    def format_to_markdown(self, plan: WeeklyPlan, shopping_list: ShoppingList) -> str:
        md = "# 🥗 Weekly Meal Plan\n\n"

        md += f"**Total Estimated Cost:** ${plan.total_estimated_cost:.2f}\n\n"

        md += "## 📅 Daily Plans\n"
        for day in plan.daily_plans:
            md += f"### Day {day.day}\n"

            # Breakfast
            md += f"#### 🍳 Breakfast: {day.breakfast.name}\n"
            md += self._format_recipe(day.breakfast)

            # Lunch
            md += f"#### 🥪 Lunch: {day.lunch.name}\n"
            md += self._format_recipe(day.lunch)

            # Dinner
            md += f"#### 🍽️ Dinner: {day.dinner.name}\n"
            md += self._format_recipe(day.dinner)

            # Snacks
            if day.snacks:
                md += "#### 🍎 Snacks\n"
                for snack in day.snacks:
                    md += f"- **{snack.name}**: {snack.nutrition.calories} cal\n"

            md += "\n---\n"

        md += "\n## 🛒 Shopping List\n"
        categories = {}
        for item in shopping_list.items:
            cat = item.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)

        for cat, items in categories.items():
            md += f"### {cat}\n"
            for item in items:
                md += f"- {item.name}: {item.quantity} {item.unit}\n"
            md += "\n"

        md += "\n## 🔪 Meal Prep Strategies\n"
        for tip in plan.meal_prep_tips:
            md += f"- {tip}\n"

        return md

    def _format_recipe(self, recipe: Recipe) -> str:
        text = f"*Prep Time: {recipe.prep_time_minutes} mins | Cost: ${recipe.estimated_cost:.2f}*\n"
        text += f"*Nutrition: {recipe.nutrition.calories} cal, {recipe.nutrition.protein_g}g protein*\n\n"
        text += "**Ingredients:**\n"
        for ing in recipe.ingredients:
            text += f"- {ing.quantity} {ing.unit} {ing.name}\n"
        text += "\n**Instructions:**\n"
        for i, step in enumerate(recipe.instructions, 1):
            text += f"{i}. {step}\n"
        text += "\n"
        return text
