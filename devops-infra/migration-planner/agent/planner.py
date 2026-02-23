import os
import json
from typing import Optional, List
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.models import MigrationPlan, BreakingChange, DataIntegrityCheck
from config import config
from prompts.system_prompts import MIGRATION_PLANNER_SYSTEM_PROMPT

class MigrationPlanner:
    def __init__(self):
        self._init_llm()

    def _init_llm(self):
        if config.LLM_PROVIDER == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model=config.MODEL_NAME,
                temperature=config.TEMPERATURE,
                google_api_key=config.GEMINI_API_KEY
            )
        else:
            self.llm = ChatOpenAI(
                model=config.MODEL_NAME,
                temperature=config.TEMPERATURE,
                openai_api_key=config.OPENAI_API_KEY
            )

    def generate_plan(self, source_schema: str, target_schema: str) -> MigrationPlan:
        """Generates a migration plan based on source and target schemas."""

        parser = PydanticOutputParser(pydantic_object=MigrationPlan)

        prompt = PromptTemplate(
            template=MIGRATION_PLANNER_SYSTEM_PROMPT,
            input_variables=["source_schema", "target_schema"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        return chain.invoke({"source_schema": source_schema, "target_schema": target_schema})

    def generate_sql_script(self, plan: MigrationPlan) -> str:
        """Generates the full SQL migration script (UP)."""
        script = [f"-- Migration Plan: {plan.summary}\n"]
        for step in plan.steps:
            script.append(f"-- Step {step.id}: {step.description}")
            script.append(f"-- Risk: {step.risk_level}, Est. Duration: {step.estimated_duration_seconds}s")
            script.append(step.sql_up)
            script.append("")
        return "\n".join(script)

    def generate_rollback_script(self, plan: MigrationPlan) -> str:
        """Generates the full SQL rollback script (DOWN)."""
        script = [f"-- Rollback Plan for: {plan.summary}\n"]
        # Reverse steps for rollback
        for step in reversed(plan.steps):
            script.append(f"-- Revert Step {step.id}: {step.description}")
            script.append(step.sql_down)
            script.append("")
        return "\n".join(script)

    def identify_breaking_changes(self, plan: MigrationPlan) -> List[BreakingChange]:
        """Returns the list of breaking changes identified in the plan."""
        return plan.breaking_changes

    def validate_data_integrity(self, plan: MigrationPlan) -> List[DataIntegrityCheck]:
        """Returns the list of data integrity checks."""
        return plan.integrity_checks
