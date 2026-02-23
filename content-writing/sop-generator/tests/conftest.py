import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    # Ensure invoke returns an AIMessage or string depending on how it's used.
    # In my code, I use `chain = prompt | llm | output_parser`.
    # The output parser expects an AIMessage or string if it's StrOutputParser.
    # Actually, StrOutputParser works on AIMessage or String.
    # But usually LLM returns AIMessage.
    llm.invoke.return_value = AIMessage(content="Mocked LLM Response")
    return llm

@pytest.fixture
def mock_output_parser():
    parser = MagicMock()
    parser.invoke.return_value = "Mocked Parsed Output"
    return parser
