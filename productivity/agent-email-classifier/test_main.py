"""Tests for Email Classifier Agent."""
import pytest
from main import run, classify


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Email Classifier" in result


class TestClassify:
    def test_urgent_email(self):
        result = classify("URGENT: Server down!", "Critical issue needs immediate attention")
        assert result["category"] == "urgent"
        assert result["priority"] == "high"

    def test_meeting_email(self):
        result = classify("Meeting invite", "Let's schedule a call")
        assert result["category"] == "meeting"

    def test_invoice_email(self):
        result = classify("Invoice #1234", "Payment due March 30")
        assert result["category"] == "invoice"

    def test_newsletter_email(self):
        result = classify("Weekly Newsletter", "Unsubscribe to stop")
        assert result["category"] == "newsletter"
        assert result["priority"] == "low"

    def test_spam_email(self):
        result = classify("Congratulations!", "You've won a free offer")
        assert result["category"] == "spam"

    def test_general_email(self):
        result = classify("Hello", "Just wanted to say hi")
        assert result["category"] == "general"

    def test_returns_action(self):
        result = classify("URGENT", "asap")
        assert "Reply" in result["action"] or "reply" in result["action"].lower()

    def test_returns_dict(self):
        result = classify("test", "body")
        assert isinstance(result, dict)
        assert "category" in result
        assert "priority" in result
        assert "action" in result
