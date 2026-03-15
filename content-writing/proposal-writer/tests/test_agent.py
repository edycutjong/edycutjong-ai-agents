import os
import sys
import json
import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.generator import ProposalGenerator
from agent.models import Proposal

@pytest.fixture
def mock_proposal_json():
    return json.dumps({
        "project_title": "Test Project",
        "executive_summary": "Summary",
        "scope_of_work": [{"title": "Scope 1", "description": "Desc 1"}],
        "timeline": [{"name": "M1", "date": "W1", "description": "Milestone 1"}],
        "budget": [{"item": "B1", "cost": 100.0, "description": "Cost 1"}],
        "deliverables": [{"name": "D1", "format": "PDF", "acceptance_criteria": "AC 1"}],
        "risks": [{"description": "Risk 1", "severity": "Low", "mitigation": "Mitigation 1"}]
    })

def test_proposal_generator_initialization():
    with patch('agent.generator.OPENAI_API_KEY', 'test-key'):
        with patch('agent.generator.ChatOpenAI'):
            generator = ProposalGenerator()
            assert generator.llm is not None
            assert generator.parser is not None
            assert generator.system_prompt is not None

def test_generate_proposal(mock_proposal_json):
    with patch('agent.generator.OPENAI_API_KEY', 'test-key'):
        with patch('agent.generator.ChatOpenAI') as MockChat:
            # We use a real RunnableLambda to mimic LLM behavior in the chain
            # because LangChain's | operator expects Runnables.

            fake_llm = RunnableLambda(lambda x: AIMessage(content=mock_proposal_json))

            # When ChatOpenAI() is called, return our fake runnable?
            # No, ChatOpenAI() returns an object.
            # But ProposalGenerator.__init__ sets self.llm = ChatOpenAI(...)

            # So we can let __init__ run with a Mock (MockChat), then replace self.llm

            generator = ProposalGenerator()
            generator.llm = fake_llm

            proposal = generator.generate_proposal("requirements")

            assert isinstance(proposal, Proposal)
            assert proposal.project_title == "Test Project"
            assert len(proposal.scope_of_work) == 1
            assert proposal.budget[0].cost == 100.0


def test_generator_raises_without_api_key():
    """Cover generator.py line 18: ValueError when OPENAI_API_KEY is empty."""
    with patch('agent.generator.OPENAI_API_KEY', ''):
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            ProposalGenerator()


def test_generate_proposal_runtime_error():
    """Cover generator.py lines 56-58: RuntimeError when chain fails."""
    with patch('agent.generator.OPENAI_API_KEY', 'test-key'):
        with patch('agent.generator.ChatOpenAI'):
            generator = ProposalGenerator()
            # Make the chain raise an exception
            generator.llm = Mock(side_effect=Exception("LLM down"))
            with pytest.raises(RuntimeError, match="Failed to generate proposal"):
                generator.generate_proposal("requirements")


def test_config_jules_api_key_fallback():
    """Cover config.py line 8: JULES_API_KEY fallback when OPENAI_API_KEY missing."""
    import importlib
    env = {"JULES_API_KEY": "jules-key"}  # No OPENAI_API_KEY
    with patch.dict(os.environ, env, clear=True), \
         patch('dotenv.load_dotenv'):
        import config as cfg_module
        importlib.reload(cfg_module)
        assert cfg_module.OPENAI_API_KEY == "jules-key"


def test_config_no_api_key():
    """Cover config.py line 18: no API key at all."""
    import importlib
    with patch.dict(os.environ, {}, clear=True), \
         patch('dotenv.load_dotenv'):
        import config as cfg_module
        importlib.reload(cfg_module)
        assert cfg_module.OPENAI_API_KEY is None
