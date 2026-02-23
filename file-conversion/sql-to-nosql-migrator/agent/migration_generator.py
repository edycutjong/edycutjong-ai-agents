import json
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .llm_engine import LLMEngine
from prompts.system_prompts import MIGRATION_SYSTEM_PROMPT

class MigrationGenerator:
    def __init__(self, llm_engine: LLMEngine):
        self.llm = llm_engine

    def generate_script(self, sql_schema: dict, nosql_schema: str, target: str, strategy: str = "embed") -> str:
        """
        Generates a Python migration script to migrate data from SQL to NoSQL.
        """
        schema_str = json.dumps(sql_schema, indent=2)

        system_prompt = MIGRATION_SYSTEM_PROMPT.format(target=target, strategy=strategy)

        user_prompt = f"""
        SQL Schema:
        {schema_str}

        Target NoSQL Schema:
        {nosql_schema}

        Generate the migration script.
        """

        response = self.llm.generate(system_prompt, user_prompt)
        return self._clean_response(response)

    def _clean_response(self, response: str) -> str:
        # Remove markdown code blocks if present
        if "```python" in response:
            response = response.split("```python")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        return response.strip()
