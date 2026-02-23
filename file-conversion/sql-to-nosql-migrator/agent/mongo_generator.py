import json
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .llm_engine import LLMEngine
from prompts.system_prompts import MONGO_SYSTEM_PROMPT

class MongoGenerator:
    def __init__(self, llm_engine: LLMEngine):
        self.llm = llm_engine

    def generate_schema(self, sql_schema: dict, strategy: str = "embed") -> str:
        """
        Generates a MongoDB schema based on the SQL schema.
        """
        schema_str = json.dumps(sql_schema, indent=2)

        system_prompt = MONGO_SYSTEM_PROMPT.format(strategy=strategy)

        user_prompt = f"""
        SQL Schema:
        {schema_str}

        Generate the MongoDB schema.
        """

        response = self.llm.generate(system_prompt, user_prompt)
        return self._clean_response(response)

    def _clean_response(self, response: str) -> str:
        # Remove markdown code blocks if present
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        return response.strip()
