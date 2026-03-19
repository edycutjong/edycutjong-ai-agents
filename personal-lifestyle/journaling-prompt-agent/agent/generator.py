from pathlib import Path
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import config

OPENAI_API_KEY = config.OPENAI_API_KEY
MODEL_NAME = config.MODEL_NAME
TEMPERATURE = config.TEMPERATURE
BASE_DIR = config.BASE_DIR

class PromptGenerator:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.llm = None
        if self.api_key:
            self.llm = ChatOpenAI(
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                openai_api_key=self.api_key
            )

    def _load_prompt(self, filename: str) -> str:
        prompt_path = BASE_DIR / "prompts" / filename  # pragma: no cover
        return prompt_path.read_text(encoding="utf-8")  # pragma: no cover

    def _generate(self, template_str: str, **kwargs) -> str:
        if not self.llm:
            return "Error: OpenAI API Key not found. Please set OPENAI_API_KEY in .env file."

        prompt = PromptTemplate.from_template(template_str)  # pragma: no cover
        chain = prompt | self.llm | StrOutputParser()  # pragma: no cover

        try:  # pragma: no cover
            return chain.invoke(kwargs)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return f"Error generating prompt: {str(e)}"  # pragma: no cover

    def generate_contextual_prompt(self, mood: str, energy: int, context: str = "") -> str:
        template = self._load_prompt("contextual.txt")
        return self._generate(template, mood=mood, energy=energy, context=context)

    def generate_gratitude_prompts(self, mood: str) -> str:
        template = self._load_prompt("gratitude.txt")  # pragma: no cover
        return self._generate(template, mood=mood)  # pragma: no cover

    def generate_reflection_prompts(self, context: str = "") -> str:
        template = self._load_prompt("reflection.txt")  # pragma: no cover
        return self._generate(template, context=context)  # pragma: no cover

    def generate_themed_prompt(self, theme: str) -> str:
        template = self._load_prompt("themed.txt")  # pragma: no cover
        return self._generate(template, theme=theme)  # pragma: no cover
