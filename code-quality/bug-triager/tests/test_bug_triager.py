import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add apps/agents/bug-triager to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Set env vars globally for tests
os.environ["OPENAI_API_KEY"] = "sk-test-key-123"
os.environ["GITHUB_TOKEN"] = "test_token"
os.environ["GITHUB_REPO"] = "owner/repo"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4"

from agents import BugTriagerAgents
from tasks import BugTriagerTasks
from tools import fetch_open_issues, apply_label, assign_user, post_comment
from crewai import Agent

class TestBugTriager:
    def test_agents_init(self):
        # Since we set OPENAI_API_KEY, Agent init should succeed even if it checks for key presence.
        # It won't make calls until execution.
        agents = BugTriagerAgents()
        triage = agents.triage_agent()
        assert triage.role == 'Bug Triage Specialist'
        assert triage.goal == 'Analyze new GitHub issues to determine appropriate labels and assignees.'

        dup = agents.duplicate_checker_agent()
        assert dup.role == 'Duplicate Issue Detective'

        resp = agents.response_agent()
        assert resp.role == 'Community Manager'

    def test_tasks_creation(self):
        tasks = BugTriagerTasks()

        # Create a real Agent to satisfy Pydantic validation
        # We use a mocked LLM to ensure no network calls during Agent init if any
        # But Agent(llm=...) expects an LLM object or string.
        # If we pass a string, it uses internal logic.
        # Let's pass the string as configured.

        agent = Agent(
            role="Test Agent",
            goal="Testing",
            backstory="Just a test",
            allow_delegation=False,
            llm="gpt-4"
        )

        task1 = tasks.analyze_issue_task(agent, "Test Issue Content")
        assert "Test Issue Content" in task1.description
        assert task1.agent == agent

        task2 = tasks.check_duplicate_task(agent, "Test Issue Content")
        assert "Test Issue Content" in task2.description

        task3 = tasks.draft_response_task(agent, "Test Issue Content", [])
        assert "Draft a polite" in task3.description

    @patch('tools.Github')
    def test_github_tools(self, mock_github):
        mock_g = MagicMock()
        mock_repo = MagicMock()
        mock_issue = MagicMock()

        mock_github.return_value = mock_g
        mock_g.get_repo.return_value = mock_repo
        mock_repo.get_issue.return_value = mock_issue

        # Test fetch_open_issues
        fetch_open_issues()
        mock_repo.get_issues.assert_called_with(state='open')

        # Test apply_label
        apply_label(1, 'bug')
        mock_repo.get_issue.assert_called_with(1)
        mock_issue.add_to_labels.assert_called_with('bug')

        # Test assign_user
        assign_user(1, 'user')
        mock_issue.add_to_assignees.assert_called_with('user')

        # Test post_comment
        post_comment(1, 'comment')
        mock_issue.create_comment.assert_called_with('comment')
