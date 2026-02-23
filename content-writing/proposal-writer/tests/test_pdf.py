import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.models import Proposal, ScopeItem, Milestone, BudgetItem, Deliverable, Risk
from agent.pdf_generator import create_pdf, create_markdown

@pytest.fixture
def sample_proposal():
    return Proposal(
        project_title="Test Project",
        executive_summary="This is a summary.",
        scope_of_work=[ScopeItem(title="Scope 1", description="Desc 1")],
        timeline=[Milestone(name="M1", date="W1", description="Milestone 1")],
        budget=[BudgetItem(item="B1", cost=100.0, description="Cost 1")],
        deliverables=[Deliverable(name="D1", format="PDF", acceptance_criteria="AC 1")],
        risks=[Risk(description="Risk 1", severity="Low", mitigation="Mitigation 1")]
    )

def test_create_markdown(sample_proposal, tmp_path):
    output_file = tmp_path / "test_proposal.md"
    create_markdown(sample_proposal, str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert "# Test Project" in content
    assert "## Executive Summary" in content
    assert "This is a summary." in content
    assert "| M1 | W1 | Milestone 1 |" in content

def test_create_pdf(sample_proposal, tmp_path):
    output_file = tmp_path / "test_proposal.pdf"
    create_pdf(sample_proposal, str(output_file))

    assert output_file.exists()
    # Verify file is not empty
    assert output_file.stat().st_size > 0
