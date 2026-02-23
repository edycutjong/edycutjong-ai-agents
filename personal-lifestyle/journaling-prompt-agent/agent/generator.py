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
        prompt_path = BASE_DIR / "prompts" / filename
        return prompt_path.read_text(encoding="utf-8")

    def _generate(self, template_str: str, **kwargs) -> str:
        if not self.llm:
            return "Error: OpenAI API Key not found. Please set OPENAI_API_KEY in .env file."

        prompt = PromptTemplate.from_template(template_str)
        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke(kwargs)
        except Exception as e:
            return f"Error generating prompt: {str(e)}"

    def generate_contextual_prompt(self, mood: str, energy: int, context: str = "") -> str:
        template = self._load_prompt("contextual.txt")
        return self._generate(template, mood=mood, energy=energy, context=context)

    def generate_gratitude_prompts(self, mood: str) -> str:
        template = self._load_prompt("gratitude.txt")
        return self._generate(template, mood=mood)

    def generate_reflection_prompts(self, context: str = "") -> str:
        template = self._load_prompt("reflection.txt")
        return self._generate(template, context=context)

    def generate_themed_prompt(self, theme: str) -> str:
        template = self._load_prompt("themed.txt")
        return self._generate(template, theme=theme)
