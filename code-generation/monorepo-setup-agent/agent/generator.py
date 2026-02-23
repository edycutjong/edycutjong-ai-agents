from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import settings
from prompts.system_prompts import (
    PACKAGE_JSON_PROMPT,
    TSCONFIG_PROMPT,
    CI_PIPELINE_PROMPT,
    README_PROMPT
)

class MonorepoGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )

    def _generate(self, prompt_template: str, context: Dict[str, Any]) -> str:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke(context)

    def generate_package_json(self, project_name: str, package_manager: str, monorepo_tool: str) -> str:
        context = {
            "project_name": project_name,
            "package_manager": package_manager,
            "monorepo_tool": monorepo_tool
        }
        return self._generate(PACKAGE_JSON_PROMPT, context)

    def generate_tsconfig(self, monorepo_tool: str) -> str:
        context = {"monorepo_tool": monorepo_tool}
        return self._generate(TSCONFIG_PROMPT, context)

    def generate_ci_config(self, ci_provider: str, package_manager: str) -> str:
        context = {
            "ci_provider": ci_provider,
            "package_manager": package_manager
        }
        return self._generate(CI_PIPELINE_PROMPT, context)

    def generate_readme(self, project_name: str, description: str) -> str:
        context = {
            "project_name": project_name,
            "description": description
        }
        return self._generate(README_PROMPT, context)
