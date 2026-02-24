import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_draft_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"subject": "Project Update - Q1 Milestones", "greeting": "Hi Team,", "body": "I wanted to share a quick update on our Q1 progress. We have completed the MVP and are on track for the beta launch next week. The test coverage is now at 90%.", "closing": "Best regards,\\nAlex", "full_draft": "Hi Team,\\n\\nI wanted to share a quick update on our Q1 progress. We have completed the MVP and are on track for the beta launch next week. The test coverage is now at 90%.\\n\\nBest regards,\\nAlex"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import EmailDraftAgent
    agent = EmailDraftAgent()
    result = agent.draft("- MVP complete\n- Beta launch next week\n- 90% test coverage", tone="formal")

    assert isinstance(result, dict)
    assert result["subject"] == "Project Update - Q1 Milestones"
    assert "MVP" in result["body"]
    assert "full_draft" in result
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_draft_strips_fences(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"subject": "Quick Check-in", "greeting": "Hey!", "body": "Just checking in on the design files.", "closing": "Cheers", "full_draft": "Hey!\\n\\nJust checking in on the design files.\\n\\nCheers"}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import EmailDraftAgent
    agent = EmailDraftAgent()
    result = agent.draft("- Check on design files", tone="casual")

    assert result["subject"] == "Quick Check-in"
    assert "design files" in result["body"]


@patch("src.agent.genai")
def test_draft_with_context(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"subject": "Re: Budget Approval", "greeting": "Dear Sarah,", "body": "Thank you for sending the budget proposal. I have reviewed it and approve the allocation for Q2. Please proceed with the vendor contracts.", "closing": "Kind regards,\\nJohn", "full_draft": "Dear Sarah,\\n\\nThank you for sending the budget proposal. I have reviewed it and approve the allocation for Q2. Please proceed with the vendor contracts.\\n\\nKind regards,\\nJohn"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import EmailDraftAgent
    agent = EmailDraftAgent()
    result = agent.draft(
        "- Approve budget\n- Proceed with vendors",
        tone="formal",
        length="medium",
        context="Sarah sent a budget proposal for Q2",
    )

    assert result["subject"] == "Re: Budget Approval"
    assert "approve" in result["body"].lower()
    assert "full_draft" in result
