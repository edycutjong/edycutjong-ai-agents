import pytest
import sys
import os

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from agent.models import Email, TriageResult
from agent.email_service import MockEmailProvider
from agent.llm_service import LLMService

def test_email_model():
    email = Email(
        id="123",
        subject="Test",
        sender="test@test.com",
        recipient="me@test.com",
        date=datetime.now(),
        body="Test Body"
    )
    assert email.id == "123"
    assert email.subject == "Test"

def test_triage_result_model():
    result = TriageResult(
        category="Urgent",
        urgency_score=10,
        summary="Test Summary",
        action_items=["Action 1"],
        suggested_actions=["Reply"]
    )
    assert result.category == "Urgent"
    assert result.urgency_score == 10

def test_mock_email_provider():
    provider = MockEmailProvider()
    provider.connect()
    emails = provider.fetch_emails(limit=5)
    assert len(emails) == 5
    assert emails[0].subject == "URGENT: Project Deadline Update"

    # Use id from fetched email
    email_id = emails[0].id
    email = provider.get_email(email_id)
    assert email is not None
    assert email.id == email_id

    email = provider.get_email("999")
    assert email is None
    provider.disconnect()

def test_llm_service_mock():
    # Force no API key for test environment to ensure mock usage or mock the env var
    # However, LLMService reads config on init.
    # We can rely on the fact that in this sandbox, OPENAI_API_KEY might not be set or we can mock it.
    # But LLMService handles missing key by falling back to mock.

    service = LLMService()
    # Force mock mode
    service.llm = None

    email = Email(
        id="1",
        subject="Urgent Task",
        sender="boss@company.com",
        recipient="me@company.com",
        date=datetime.now(),
        body="Do this now."
    )

    result = service.analyze_email(email)
    assert isinstance(result, TriageResult)
    # The mock implementation checks for "urgent" in subject (case insensitive)
    assert result.category == "Urgent"

    reply = service.draft_reply(email)
    assert "mock reply" in reply.lower()

    briefing = service.generate_briefing([email])
    assert "mock daily briefing" in briefing.lower() or "no high-priority" in briefing.lower()
