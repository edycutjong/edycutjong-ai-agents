from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any, Generator, Tuple

from .analyzer import analyze_code_structure, analyze_text_content
from prompts.templates import (
    INTRODUCTION_TEMPLATE,
    PREREQUISITES_TEMPLATE,
    OUTLINE_TEMPLATE,
    SECTION_CONTENT_TEMPLATE,
    CODE_EXAMPLE_TEMPLATE,
    TROUBLESHOOTING_TEMPLATE,
)

class TutorialGenerator:
    def __init__(self, api_key: str, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(api_key=api_key, model=model_name, temperature=0.7)
        self.output_parser = StrOutputParser()
        self.context = ""

    def analyze_input(self, text: str, is_code: bool = False) -> str:
        """Analyzes input and stores context."""
        if is_code:
            structure = analyze_code_structure(text)
            # Convert structure to string representation for LLM context
            self.context = f"Code Structure Analysis:\n{structure}"
        else:
            self.context = analyze_text_content(text, self.llm)
        return self.context

    def generate_introduction(self, difficulty: str) -> str:
        chain = INTRODUCTION_TEMPLATE | self.llm | self.output_parser
        return chain.invoke({"context": self.context, "difficulty": difficulty})

    def generate_prerequisites(self, difficulty: str) -> str:
        chain = PREREQUISITES_TEMPLATE | self.llm | self.output_parser
        return chain.invoke({"context": self.context, "difficulty": difficulty})

    def generate_outline(self, difficulty: str, topic: str) -> str:
        chain = OUTLINE_TEMPLATE | self.llm | self.output_parser
        return chain.invoke({"context": self.context, "difficulty": difficulty, "topic": topic})

    def generate_section_content(self, section_title: str, section_goal: str, difficulty: str) -> str:
        chain = SECTION_CONTENT_TEMPLATE | self.llm | self.output_parser
        return chain.invoke({
            "context": self.context,
            "section_title": section_title,
            "section_goal": section_goal,
            "difficulty": difficulty
        })

    def generate_code_example(self, topic: str) -> str:
        chain = CODE_EXAMPLE_TEMPLATE | self.llm | self.output_parser
        return chain.invoke({"context": self.context, "topic": topic})

    def generate_troubleshooting(self) -> str:
        chain = TROUBLESHOOTING_TEMPLATE | self.llm | self.output_parser
        return chain.invoke({"context": self.context})

    def generate_full_tutorial_stream(self, text: str, difficulty: str, topic: str, is_code: bool = False) -> Generator[Tuple[str, str], None, None]:
        """Generator that yields sections as they are created."""
        # 1. Analysis
        yield ("Analysis", self.analyze_input(text, is_code))

        # 2. Introduction
        yield ("Introduction", self.generate_introduction(difficulty))

        # 3. Prerequisites
        yield ("Prerequisites", self.generate_prerequisites(difficulty))

        # 4. Outline (Internal or Displayed) - we display it as part of structure
        outline = self.generate_outline(difficulty, topic)
        yield ("Outline", outline)

        # 5. Step-by-Step Guide
        # Using the outline as context/goal implicitly by asking for detailed steps based on context
        yield ("Step-by-Step Guide", self.generate_section_content("Step-by-Step Guide", "Provide detailed steps to achieve the goal.", difficulty))

        # 6. Runnable Code Example
        yield ("Code Example", self.generate_code_example(topic))

        # 7. Troubleshooting
        yield ("Troubleshooting", self.generate_troubleshooting())
