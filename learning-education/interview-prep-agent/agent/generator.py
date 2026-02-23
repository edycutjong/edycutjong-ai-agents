from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import List, Optional, Union
from .models import CodingQuestion, SystemDesignQuestion, BehavioralQuestion
from prompts.templates import CODING_QUESTION_TEMPLATE, SYSTEM_DESIGN_TEMPLATE, BEHAVIORAL_TEMPLATE
from config import MODEL_NAME, TEMPERATURE

class QuestionGenerator:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(api_key=api_key, model=MODEL_NAME, temperature=TEMPERATURE)

    def generate_coding_question(self, skills: List[str], experience_level: str, difficulty: str = "Medium") -> Optional[CodingQuestion]:
        """
        Generates a coding question based on skills and experience level.
        """
        parser = PydanticOutputParser(pydantic_object=CodingQuestion)
        prompt = ChatPromptTemplate.from_template(CODING_QUESTION_TEMPLATE + "\n\n{format_instructions}")

        chain = prompt | self.llm | parser
        try:
            return chain.invoke({
                "skills": ", ".join(skills),
                "experience_level": experience_level,
                "difficulty": difficulty,
                "format_instructions": parser.get_format_instructions()
            })
        except Exception as e:
            print(f"Error generating coding question: {e}")
            return None

    def generate_system_design_question(self, skills: List[str], experience_level: str) -> Optional[SystemDesignQuestion]:
        """
        Generates a system design question.
        """
        parser = PydanticOutputParser(pydantic_object=SystemDesignQuestion)
        prompt = ChatPromptTemplate.from_template(SYSTEM_DESIGN_TEMPLATE + "\n\n{format_instructions}")

        chain = prompt | self.llm | parser
        try:
            return chain.invoke({
                "skills": ", ".join(skills),
                "experience_level": experience_level,
                "format_instructions": parser.get_format_instructions()
            })
        except Exception as e:
            print(f"Error generating system design question: {e}")
            return None

    def generate_behavioral_question(self, focus_area: str = "Leadership") -> Optional[BehavioralQuestion]:
        """
        Generates a behavioral question.
        """
        parser = PydanticOutputParser(pydantic_object=BehavioralQuestion)
        prompt = ChatPromptTemplate.from_template(BEHAVIORAL_TEMPLATE + "\n\n{format_instructions}")

        chain = prompt | self.llm | parser
        try:
            return chain.invoke({
                "focus_area": focus_area,
                "format_instructions": parser.get_format_instructions()
            })
        except Exception as e:
            print(f"Error generating behavioral question: {e}")
            return None
