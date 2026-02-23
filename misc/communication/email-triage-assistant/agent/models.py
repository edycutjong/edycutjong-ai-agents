from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Email(BaseModel):
    id: str
    subject: str
    sender: str
    recipient: str
    date: datetime
    body: str
    snippet: Optional[str] = None
    folder: str = "INBOX"

class TriageResult(BaseModel):
    category: str = Field(description="The category of the email (e.g., Urgent, Work, Personal, Newsletter, Spam)")
    urgency_score: int = Field(description="Urgency score from 1 (low) to 10 (high)")
    summary: str = Field(description="A brief summary of the email content")
    action_items: List[str] = Field(default_factory=list, description="List of action items extracted from the email")
    suggested_actions: List[str] = Field(default_factory=list, description="Suggested next steps")

class DraftReply(BaseModel):
    subject: str
    body: str
    tone: str = "professional"

class DailyBriefing(BaseModel):
    date: datetime
    total_emails: int
    urgent_count: int
    top_items: List[TriageResult]
    summary: str
