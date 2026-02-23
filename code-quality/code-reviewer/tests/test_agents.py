import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents import CodeReviewerAgents
from src.tasks import CodeReviewerTasks
from agent_config import Config

@pytest.fixture
def mock_config():
    with patch.object(Config, 'OPENAI_API_KEY', 'fake_key'):
        yield

@patch('src.agents.Agent')
@patch('src.agents.ChatOpenAI')
def test_agents_initialization(mock_chat_openai, mock_agent, mock_config):
    mock_agent_instance = MagicMock()
    mock_agent.return_value = mock_agent_instance

    agents = CodeReviewerAgents()

    # Test code_reviewer_agent
    reviewer = agents.code_reviewer_agent()
    assert reviewer == mock_agent_instance
    mock_agent.assert_called_with(
        role='Senior Code Reviewer',
        goal='Ensure code quality, readability, and correct logic implementation.',
        backstory='You are an expert software engineer with years of experience in reviewing code. You focus on logic, potential bugs, and maintainability.',
        llm=agents.llm,
        verbose=True
    )

    # Test style_checker_agent
    style_checker = agents.style_checker_agent()
    assert style_checker == mock_agent_instance
    mock_agent.assert_called_with(
        role='Style Guide Enforcer',
        goal='Ensure code adheres to standard style guides (e.g., PEP8 for Python, ESLint rules for JS).',
        backstory='You are meticulous about code style and formatting. You ensure consistency across the codebase.',
        llm=agents.llm,
        verbose=True
    )

    # Test security_analyst_agent
    security = agents.security_analyst_agent()
    assert security == mock_agent_instance
    mock_agent.assert_called_with(
        role='Security Analyst',
        goal='Identify potential security vulnerabilities in the code.',
        backstory='You are a security expert. You look for injection flaws, sensitive data exposure, and other security risks.',
        llm=agents.llm,
        verbose=True
    )

    # Test report_generator_agent
    report_gen = agents.report_generator_agent()
    assert report_gen == mock_agent_instance
    mock_agent.assert_called_with(
        role='Review Summary Generator',
        goal='Synthesize multiple technical reviews into a cohesive, structured report.',
        backstory='You are an expert technical writer. You take findings from code reviewers, style checkers, and security analysts and compile them into a clear, actionable report.',
        llm=agents.llm,
        verbose=True
    )

@patch('src.tasks.Task')
def test_tasks_creation(mock_task):
    tasks = CodeReviewerTasks()
    agent = MagicMock()
    diff = "some diff"
    context = [MagicMock()]

    mock_task_instance = MagicMock()
    mock_task.return_value = mock_task_instance

    task1 = tasks.code_review_task(agent, diff)
    assert task1 == mock_task_instance
    _, kwargs = mock_task.call_args
    assert kwargs['agent'] == agent
    assert "Code Diff" in kwargs['description']

    task2 = tasks.style_check_task(agent, diff)
    assert task2 == mock_task_instance
    _, kwargs = mock_task.call_args
    assert kwargs['agent'] == agent

    task3 = tasks.security_audit_task(agent, diff)
    assert task3 == mock_task_instance
    _, kwargs = mock_task.call_args
    assert kwargs['agent'] == agent

    task4 = tasks.generate_report_task(agent, context)
    assert task4 == mock_task_instance
    _, kwargs = mock_task.call_args
    assert kwargs['agent'] == agent
    assert kwargs['context'] == context
