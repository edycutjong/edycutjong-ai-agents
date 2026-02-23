from langchain_core.prompts import ChatPromptTemplate
from prompts.templates import get_formula_prompt, FORMULA_SYSTEM_PROMPT

def test_get_formula_prompt_structure():
    """Verify that get_formula_prompt returns a ChatPromptTemplate with correct messages."""
    prompt = get_formula_prompt()

    assert isinstance(prompt, ChatPromptTemplate)
    assert len(prompt.messages) == 2

    # Check message types and contents
    assert prompt.messages[0].prompt.template == FORMULA_SYSTEM_PROMPT
    assert prompt.messages[1].prompt.template == "{query}"

def test_formula_system_prompt_content():
    """Verify that the system prompt contains key instructions."""
    prompt = FORMULA_SYSTEM_PROMPT

    # Check for key phrases required by the spec
    assert "modern functions" in prompt
    assert "XLOOKUP" in prompt
    assert "step-by-step" in prompt
    assert "syntactically correct" in prompt
    assert "{target_application}" in prompt
