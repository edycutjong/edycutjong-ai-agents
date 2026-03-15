"""Tests for MonorepoGenerator."""
import pytest
from unittest.mock import patch, MagicMock
from agent.generator import MonorepoGenerator


@patch("agent.generator.ChatOpenAI")
def test_generator_init(mock_chat):
    """Cover generator.py line 16: __init__."""
    gen = MonorepoGenerator()
    assert gen.llm is not None
    mock_chat.assert_called_once()


@patch("agent.generator.ChatOpenAI")
def test_generate_method(mock_chat):
    """Cover generator.py lines 23-25: _generate private method."""
    gen = MonorepoGenerator()
    # Mock the chain pipeline
    with patch("agent.generator.ChatPromptTemplate") as mock_prompt, \
         patch("agent.generator.StrOutputParser") as mock_parser:
        mock_prompt_inst = mock_prompt.from_template.return_value
        mock_intermediate = MagicMock()
        mock_prompt_inst.__or__ = MagicMock(return_value=mock_intermediate)
        mock_chain = MagicMock()
        mock_intermediate.__or__ = MagicMock(return_value=mock_chain)
        mock_chain.invoke.return_value = "generated content"

        result = gen._generate("template {var}", {"var": "value"})
        assert result == "generated content"


@patch("agent.generator.ChatOpenAI")
def test_generate_package_json(mock_chat):
    """Cover generator.py lines 28-33."""
    gen = MonorepoGenerator()
    with patch.object(gen, '_generate', return_value='{"name": "test"}') as mock_gen:
        result = gen.generate_package_json("test", "pnpm", "turbo")
        assert result == '{"name": "test"}'
        mock_gen.assert_called_once()
        ctx = mock_gen.call_args[0][1]
        assert ctx["project_name"] == "test"
        assert ctx["package_manager"] == "pnpm"
        assert ctx["monorepo_tool"] == "turbo"


@patch("agent.generator.ChatOpenAI")
def test_generate_tsconfig(mock_chat):
    """Cover generator.py lines 36-37."""
    gen = MonorepoGenerator()
    with patch.object(gen, '_generate', return_value='{}') as mock_gen:
        result = gen.generate_tsconfig("turbo")
        assert result == '{}'
        ctx = mock_gen.call_args[0][1]
        assert ctx["monorepo_tool"] == "turbo"


@patch("agent.generator.ChatOpenAI")
def test_generate_ci_config(mock_chat):
    """Cover generator.py lines 40-44."""
    gen = MonorepoGenerator()
    with patch.object(gen, '_generate', return_value='steps: []') as mock_gen:
        result = gen.generate_ci_config("github-actions", "pnpm")
        assert result == 'steps: []'
        ctx = mock_gen.call_args[0][1]
        assert ctx["ci_provider"] == "github-actions"
        assert ctx["package_manager"] == "pnpm"


@patch("agent.generator.ChatOpenAI")
def test_generate_readme(mock_chat):
    """Cover generator.py lines 47-51."""
    gen = MonorepoGenerator()
    with patch.object(gen, '_generate', return_value='# README') as mock_gen:
        result = gen.generate_readme("test-project", "A monorepo")
        assert result == '# README'
        ctx = mock_gen.call_args[0][1]
        assert ctx["project_name"] == "test-project"
        assert ctx["description"] == "A monorepo"
