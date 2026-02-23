from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os
from .diff_engine import APIChange

class ImpactAnalysis(BaseModel):
    summary: str = Field(description="A human-readable summary of the changes.")
    impact_level: str = Field(description="High, Medium, or Low impact on clients.")
    breaking: bool = Field(description="Whether the changes are breaking.")
    version_bump: str = Field(description="suggested version bump: MAJOR, MINOR, or PATCH.")
    changelog_entry: str = Field(description="A markdown formatted changelog entry.")

class AIAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
             print("Warning: OPENAI_API_KEY not found. AI features will be disabled.")

        self.llm = ChatOpenAI(model="gpt-4o", api_key=self.api_key) if self.api_key else None

    def analyze(self, changes: List[APIChange]) -> ImpactAnalysis:
        if not changes:
            return ImpactAnalysis(
                summary="No changes detected.",
                impact_level="None",
                breaking=False,
                version_bump="NONE",
                changelog_entry="No changes."
            )

        if not self.llm:
            # Fallback logic if no API key
            is_breaking = any(c.change_type.name == "BREAKING" for c in changes)
            return ImpactAnalysis(
                summary="AI Analysis unavailable (No API Key).",
                impact_level="High" if is_breaking else "Low",
                breaking=is_breaking,
                version_bump="MAJOR" if is_breaking else "MINOR",
                changelog_entry="\n".join([f"- {c.description}" for c in changes])
            )

        # Prepare the prompt
        changes_text = "\n".join([str(c) for c in changes])

        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert API developer and technical writer.
            Analyze the following list of API changes between two versions of an OpenAPI specification.

            Changes:
            {changes}

            Provide a structured analysis including:
            1. A summary of what changed.
            2. The impact level on consumers (High/Medium/Low).
            3. Whether it constitutes a breaking change.
            4. The recommended Semantic Versioning bump (MAJOR, MINOR, or PATCH).
            5. A professional changelog entry in Markdown.
            """
        )

        structured_llm = self.llm.with_structured_output(ImpactAnalysis)
        chain = prompt | structured_llm

        return chain.invoke({"changes": changes_text})
