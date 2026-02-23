from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import Config
from prompts.system_prompts import COPY_EDITOR_SYSTEM_PROMPT

class EditingReport(BaseModel):
    grammar_fixes: List[str] = Field(description="List of key grammar corrections")
    style_changes: List[str] = Field(description="List of changes made for style compliance")
    conciseness_improvements: List[str] = Field(description="Examples of simplified phrases")
    passive_voice_detected: List[str] = Field(description="List of sentences converted from passive to active")
    tone_adjustments: List[str] = Field(description="Notes on how tone was adjusted")

class EditorOutput(BaseModel):
    edited_text: str = Field(description="The fully edited version of the text")
    summary_report: EditingReport = Field(description="Detailed report of the edits made")

class CopyEditorAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        # If API key is still None, we might want to handle it or let LangChain raise error

        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE

        if not self.api_key:
             # Placeholder for when key is missing to avoid immediate crash on init,
             # but methods will fail.
             self.llm = None
        else:
            self.llm = ChatOpenAI(
                api_key=self.api_key,
                model=self.model_name,
                temperature=self.temperature
            )

        self.parser = JsonOutputParser(pydantic_object=EditorOutput)

    def edit_text(self, text: str, style_guide: str = Config.DEFAULT_STYLE_GUIDE, tone: str = Config.DEFAULT_TONE) -> Dict[str, Any]:
        """
        Edits the text using the LLM agent.
        """
        if not self.llm:
            raise ValueError("OpenAI API Key is missing. Please provide it in the .env file or UI.")

        # Updated prompt template to include input variables
        prompt = ChatPromptTemplate.from_template(COPY_EDITOR_SYSTEM_PROMPT)

        chain = prompt | self.llm | self.parser

        result = chain.invoke({
            "style_guide": style_guide,
            "tone": tone,
            "text": text
        })

        return result
