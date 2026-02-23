from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import Optional, Union
from .models import Evaluation
from prompts.templates import GRADING_TEMPLATE
from config import MODEL_NAME, TEMPERATURE

class ResponseGrader:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(api_key=api_key, model=MODEL_NAME, temperature=0) # Grading should be objective

    def grade_response(self, question: str, user_answer: str, question_type: str = "coding") -> Optional[Evaluation]:
        """
        Grades a user's answer to an interview question.
        """
        parser = PydanticOutputParser(pydantic_object=Evaluation)

        prompt = ChatPromptTemplate.from_template(GRADING_TEMPLATE + "\n\n{format_instructions}")

        chain = prompt | self.llm | parser

        try:
            return chain.invoke({
                "question": question,
                "answer": user_answer, # Template uses answer
                "question_type": question_type, # Template doesn't use this but it might be useful context if added
                "format_instructions": parser.get_format_instructions()
            })
        except Exception as e:
            print(f"Error grading response: {e}")
            return None
