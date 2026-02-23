import os
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class CalendarCheckInput(BaseModel):
    date_str: str = Field(description="The date to check availability for, in YYYY-MM-DD format.")

class CalendarTool(BaseTool):
    name: str = "check_calendar"
    description: str = "Checks the calendar for availability on a specific date."
    args_schema: Type[BaseModel] = CalendarCheckInput

    def _run(self, date_str: str) -> str:
        # Mock implementation
        if "2023-10-25" in date_str:
            return "Busy: Meeting with Client A at 10:00 AM."
        elif "2023-10-26" in date_str:
            return "Free all day."
        else:
            return "Free: No events scheduled."

    async def _arun(self, date_str: str) -> str:
        return self._run(date_str)

class SaveDraftInput(BaseModel):
    draft_text: str = Field(description="The text of the email draft to save.")
    recipient: str = Field(description="The recipient of the email.")

class SaveDraftTool(BaseTool):
    name: str = "save_draft"
    description: str = "Saves the drafted email to a file."
    args_schema: Type[BaseModel] = SaveDraftInput

    def _run(self, draft_text: str, recipient: str) -> str:
        # clean recipient for filename
        safe_recipient = "".join([c for c in recipient if c.isalnum() or c in (' ', '_', '-')]).strip().replace(' ', '_')
        filename = f"draft_to_{safe_recipient}.txt"
        with open(filename, "w") as f:
            f.write(draft_text)
        return f"Draft saved to {filename}"

    async def _arun(self, draft_text: str, recipient: str) -> str:
        return self._run(draft_text, recipient)

def get_llm():
    # If API key is not present, ChatOpenAI might raise an error upon instantiation or usage.
    # We will rely on environment variables being set or mocked.
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
