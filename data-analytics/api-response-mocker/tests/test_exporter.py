import pytest
from agent.exporter import PostmanExporter
from agent.parser import OpenAPIParser
import os
import json

@pytest.fixture
def parser():
    spec_path = os.path.join(os.path.dirname(__file__), 'sample_spec.yaml')
    with open(spec_path, 'r') as f:
        spec_content = f.read()
    return OpenAPIParser(spec_content)

def test_export(parser):
    exporter = PostmanExporter(parser)
    collection = exporter.export()

    assert "info" in collection
    assert collection["info"]["name"] == "Sample API"
    assert len(collection["item"]) > 0

    item = collection["item"][0]
    assert "name" in item
    assert "request" in item
    assert item["request"]["method"] in ["GET", "POST"]
