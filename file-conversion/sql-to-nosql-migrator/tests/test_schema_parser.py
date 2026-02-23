import sys
import os
import pytest

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.schema_parser import SchemaParser

def test_schema_parser_simple():
    sql = """
    CREATE TABLE users (
        id INT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100)
    );
    """
    parser = SchemaParser()
    schema = parser.parse(sql)

    assert "users" in schema
    table = schema["users"]
    assert len(table["columns"]) == 3
    assert table["columns"][0]["name"] == "id"
    assert table["columns"][0]["type"] == "INT"
    assert table["columns"][0]["pk"] is True

    assert table["columns"][1]["name"] == "username"
    assert table["columns"][1]["not_null"] is True

def test_schema_parser_multiple_tables():
    sql = """
    CREATE TABLE users (
        id INT
    );

    CREATE TABLE posts (
        id INT,
        user_id INT
    );
    """
    parser = SchemaParser()
    schema = parser.parse(sql)

    assert "users" in schema
    assert "posts" in schema
