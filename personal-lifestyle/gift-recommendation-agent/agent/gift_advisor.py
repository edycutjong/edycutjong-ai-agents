import json
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

from agent.tools import SearchTool
from prompts.system_prompts import SYSTEM_PROMPT, GIFT_GUIDE_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GiftSuggestion(BaseModel):
    name: str = Field(description="Name of the gift item")
    category: str = Field(description="Category of the gift")
    reasoning: str = Field(description="Why this gift is recommended")
    estimated_price: str = Field(description="Estimated price of the gift")
    search_query: str = Field(description="Search query to find the gift")
    purchase_link: Optional[str] = Field(default=None, description="URL to purchase the gift")

class GiftResponse(BaseModel):
    gifts: List[GiftSuggestion]

class GiftAdvisor:
    def __init__(self, api_key: Optional[str] = None):
        self.search_tool = SearchTool()
        # Ensure data directory exists
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.history_file = os.path.join(self.data_dir, "history.json")

        # Initialize LLM
        openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            self.llm = ChatOpenAI(
                temperature=0.7,
                model_name=os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
                openai_api_key=openai_api_key
            )
            self.parser = JsonOutputParser(pydantic_object=GiftResponse)
        else:
            self.llm = None
            logger.warning("OpenAI API Key not provided. Agent functionality will be limited.")

    def generate_suggestions(self, profile: Dict, occasion: str, budget: str) -> List[GiftSuggestion]:
        if not self.llm:
            raise ValueError("OpenAI API Key is required to generate suggestions.")

        logger.info(f"Generating suggestions for {profile} on {occasion} with budget {budget}")

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", "Recipient Profile: {profile}\nOccasion: {occasion}\nBudget: {budget}")
        ])

        chain = prompt | self.llm | self.parser

        try:
            profile_str = json.dumps(profile, indent=2)
            result = chain.invoke({"profile": profile_str, "occasion": occasion, "budget": budget})

            suggestions = []
            for item in result.get("gifts", []):
                suggestion = GiftSuggestion(**item)
                # Attempt to find a link
                try:
                    search_results = self.search_tool.search_gift_links(suggestion.search_query)
                    # Simple heuristic to extract first link if possible, or just pass the search query
                    # DuckDuckGoSearchResults returns stringified list of dicts with 'link' key usually
                    # But parsing that string is fragile. Let's just create a direct search URL for robustness.
                    suggestion.purchase_link = f"https://duckduckgo.com/?q={suggestion.search_query.replace(' ', '+')}&ia=web"
                except Exception as e:
                    logger.error(f"Search failed for {suggestion.name}: {e}")
                    suggestion.purchase_link = f"https://www.google.com/search?q={suggestion.search_query.replace(' ', '+')}"

                suggestions.append(suggestion)

            # Save to history automatically
            self.save_history(profile, occasion, suggestions)

            return suggestions

        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            raise e

    def generate_gift_guide(self, suggestions: List[GiftSuggestion], recipient_name: str, occasion: str) -> str:
        if not self.llm:
            return "Error: API Key missing."

        suggestions_text = "\n".join([f"- {s.name} ({s.estimated_price}): {s.reasoning}" for s in suggestions])

        prompt = ChatPromptTemplate.from_messages([
            ("system", GIFT_GUIDE_PROMPT),
            ("user", "Recipient: {recipient}\nOccasion: {occasion}\nSuggestions:\n{suggestions}")
        ])

        chain = prompt | self.llm
        response = chain.invoke({"recipient": recipient_name, "occasion": occasion, "suggestions": suggestions_text})
        return response.content

    def save_history(self, profile: Dict, occasion: str, suggestions: List[GiftSuggestion]):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "profile": profile,
            "occasion": occasion,
            "suggestions": [s.model_dump() for s in suggestions]
        }

        history = self.load_history()
        history.append(entry)

        try:
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def load_history(self) -> List[Dict]:
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            return []
