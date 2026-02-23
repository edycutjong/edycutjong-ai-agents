import pytest
from sqlalchemy import create_engine
import os
import sys

# Ensure apps/agents/sql-query-builder-agent is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def db_uri():
    return "sqlite:///:memory:"

@pytest.fixture
def engine(db_uri):
    engine = create_engine(db_uri)
    return engine
