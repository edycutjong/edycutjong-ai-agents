import sys
import os
import pytest
from unittest.mock import MagicMock

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.converter import Converter
from config import config

def test_converter_mongo():
    config.USE_MOCK_LLM = True
    converter = Converter()
    sql = "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));"
    result = converter.run(sql, "mongodb", "embed")
    assert "sql_schema" in result
    assert "nosql_schema" in result
    assert "migration_script" in result
    assert "documentation" in result
    assert "users" in result["sql_schema"]
    assert "collection" in result["nosql_schema"]

def test_converter_dynamo():
    config.USE_MOCK_LLM = True
    converter = Converter()
    sql = "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));"
    result = converter.run(sql, "dynamodb", "single-table")
    assert "TableName" in result["nosql_schema"]

def test_converter_invalid_sql():
    converter = Converter()
    sql = "INVALID SQL STATEMENT"
    result = converter.run(sql, "mongodb")
    # SchemaParser returns empty dict for invalid SQL usually, or fails silently
    # My SchemaParser returns {} if no tables found.
    assert "error" in result
    assert "Failed to parse SQL" in result["error"]

def test_converter_unsupported_db():
    config.USE_MOCK_LLM = True
    converter = Converter()
    sql = "CREATE TABLE users (id INT);"
    result = converter.run(sql, "cassandra")
    assert "error" in result
    assert "Unsupported target database" in result["error"]
