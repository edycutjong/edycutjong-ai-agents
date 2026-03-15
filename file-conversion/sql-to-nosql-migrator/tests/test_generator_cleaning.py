import pytest
import os
import sys
from unittest.mock import MagicMock

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.dynamo_generator import DynamoGenerator
from agent.mongo_generator import MongoGenerator
from agent.migration_generator import MigrationGenerator

def test_clean_response_dynamo():
    gen = DynamoGenerator(MagicMock())
    assert gen._clean_response("```json\n{keys}\n```") == "{keys}"
    assert gen._clean_response("```\n{keys}\n```") == "{keys}"
    assert gen._clean_response("{keys}") == "{keys}"

def test_clean_response_mongo():
    gen = MongoGenerator(MagicMock())
    assert gen._clean_response("```json\n{keys}\n```") == "{keys}"
    assert gen._clean_response("```\n{keys}\n```") == "{keys}"
    assert gen._clean_response("{keys}") == "{keys}"

def test_clean_response_migration():
    gen = MigrationGenerator(MagicMock())
    assert gen._clean_response("```python\nprint(1)\n```") == "print(1)"
    assert gen._clean_response("```\nprint(1)\n```") == "print(1)"
    assert gen._clean_response("print(1)") == "print(1)"
