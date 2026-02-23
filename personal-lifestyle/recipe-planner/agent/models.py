from typing import List, Optional
from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient")
    quantity: float = Field(description="Quantity of the ingredient")
    unit: str = Field(description="Unit of measurement (e.g., cups, grams, tbsp)")

class NutritionInfo(BaseModel):
    calories: int = Field(description="Approximate calories")
    protein_g: int = Field(description="Protein in grams")
    carbs_g: int = Field(description="Carbohydrates in grams")
    fat_g: int = Field(description="Fat in grams")

class Recipe(BaseModel):
    name: str = Field(description="Name of the recipe")
    ingredients: List[Ingredient] = Field(description="List of ingredients needed")
    instructions: List[str] = Field(description="Step-by-step instructions")
    nutrition: NutritionInfo = Field(description="Nutritional information per serving")
    estimated_cost: float = Field(description="Estimated cost in USD")
    prep_time_minutes: int = Field(description="Preparation time in minutes")

class DailyPlan(BaseModel):
    day: int = Field(description="Day number (1-7)")
    breakfast: Recipe
    lunch: Recipe
    dinner: Recipe
    snacks: List[Recipe] = Field(description="List of snack options")

class WeeklyPlan(BaseModel):
    daily_plans: List[DailyPlan] = Field(description="List of daily meal plans")
    meal_prep_tips: List[str] = Field(description="Strategies for efficient meal prepping")
    total_estimated_cost: float = Field(description="Total estimated cost for the week")

class ShoppingItem(BaseModel):
    name: str
    quantity: float
    unit: str
    category: str = Field(description="Category (e.g., Produce, Dairy, Meat)")

class ShoppingList(BaseModel):
    items: List[ShoppingItem] = Field(description="Consolidated list of items to buy")
