import json
import os
import pytest
from agent.parser import FigmaParser

@pytest.fixture
def sample_data():
    path = os.path.join(os.path.dirname(__file__), "data/mock_figma.json")
    with open(path, "r") as f:
        return json.load(f)

def test_parser_init(sample_data):
    parser = FigmaParser(sample_data)
    assert parser.document["type"] == "DOCUMENT"

def test_parser_parse(sample_data):
    parser = FigmaParser(sample_data)
    nodes = parser.parse()

    # Expect 2 nodes: Frame (My Button) and Text (Label)
    # The Document and Canvas are typically skipped by _is_relevant_node or don't have styles
    # Let's check logic:
    # _is_relevant_node checks: FRAME, GROUP, TEXT...
    # Document type is DOCUMENT (not in list)
    # Canvas type is CANVAS (not in list)
    # My Button is FRAME (in list)
    # Label is TEXT (in list)

    assert len(nodes) == 2

    frame_node = next(n for n in nodes if n["type"] == "FRAME")
    assert frame_node["name"] == "My Button"
    assert "background-color" in frame_node["styles"]
    assert frame_node["styles"]["border-radius"] == "8px"
    assert frame_node["layout"]["display"] == "flex"

    text_node = next(n for n in nodes if n["type"] == "TEXT")
    assert text_node["name"] == "Label"
    assert text_node["styles"]["font-family"] == "'Inter'"
    assert text_node["styles"]["font-size"] == "16px"
