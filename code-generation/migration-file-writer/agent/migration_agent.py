import os
import sys

# Add parent directory to path to allow imports from config and prompts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from config import Config
    from prompts.system_prompts import (
        PRISMA_MIGRATION_PROMPT,
        ALEMBIC_MIGRATION_PROMPT,
        KNEX_MIGRATION_PROMPT,
        ROLLBACK_PROMPT,
        SAFETY_ANALYSIS_PROMPT,
    )
except ImportError:
    # Fallback for when running from a different context
    from apps.agents.code_generation.migration_file_writer.config import Config
    from apps.agents.code_generation.migration_file_writer.prompts.system_prompts import (
        PRISMA_MIGRATION_PROMPT,
        ALEMBIC_MIGRATION_PROMPT,
        KNEX_MIGRATION_PROMPT,
        ROLLBACK_PROMPT,
        SAFETY_ANALYSIS_PROMPT,
    )

class MigrationAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        if self.api_key:
            self.llm = ChatOpenAI(
                model=Config.MODEL_NAME,
                temperature=Config.TEMPERATURE,
                api_key=self.api_key,
            )
        else:
            self.llm = None  # Handle missing key gracefully

    def generate_migration(self, old_schema: str, new_schema: str, orm_type: str) -> str:
        if not self.llm:
            return "Error: OpenAI API Key not found. Please set OPENAI_API_KEY in .env or provide it."

        prompt_template = ""
        if orm_type.lower() == "prisma":
            prompt_template = PRISMA_MIGRATION_PROMPT
        elif orm_type.lower() == "alembic":
            prompt_template = ALEMBIC_MIGRATION_PROMPT
        elif orm_type.lower() == "knex":
            prompt_template = KNEX_MIGRATION_PROMPT
        else:
            return f"Error: Unsupported ORM type '{orm_type}'."

        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_template),
            ("user", "Old Schema:\n{old_schema}\n\nNew Schema:\n{new_schema}")
        ])

        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"old_schema": old_schema, "new_schema": new_schema})

    def generate_rollback(self, migration_code: str, orm_type: str) -> str:
        if not self.llm:
            return "Error: OpenAI API Key not found."

        prompt = ChatPromptTemplate.from_messages([
            ("system", ROLLBACK_PROMPT),
            ("user", "Migration Code:\n{migration_code}\n\nORM Type: {orm_type}")
        ])

        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"migration_code": migration_code, "orm_type": orm_type})

    def analyze_safety(self, migration_code: str, old_schema: str, new_schema: str) -> str:
        if not self.llm:
            return "Error: OpenAI API Key not found."

        prompt = ChatPromptTemplate.from_messages([
            ("system", SAFETY_ANALYSIS_PROMPT),
            ("user", "Migration Code:\n{migration_code}\n\nOld Schema:\n{old_schema}\n\nNew Schema:\n{new_schema}")
        ])

        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "migration_code": migration_code,
            "old_schema": old_schema,
            "new_schema": new_schema
        })
