from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import ValidationError
from typing import Optional
from .models import JobDescription
from prompts.templates import PARSER_TEMPLATE
from config import MODEL_NAME, TEMPERATURE

class JobParser:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(api_key=api_key, model=MODEL_NAME, temperature=0) # Parser usually benefits from low temp
        self.parser = PydanticOutputParser(pydantic_object=JobDescription)

    def parse(self, job_text: str) -> Optional[JobDescription]:
        """
        Parses a job description text into a structured JobDescription object.
        """
        prompt = ChatPromptTemplate.from_template(PARSER_TEMPLATE + "\n\n{format_instructions}")

        chain = prompt | self.llm | self.parser

        try:
            return chain.invoke({
                "job_description": job_text, # Template uses job_description
                "format_instructions": self.parser.get_format_instructions()
            })
        except ValidationError as e:  # pragma: no cover
            # Handle parsing errors gracefully
            print(f"Parsing error: {e}")  # pragma: no cover
            return None  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print(f"Error during LLM call: {e}")  # pragma: no cover
            return None  # pragma: no cover
