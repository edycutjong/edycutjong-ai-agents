import pytest
import os
import sys
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch.dict('sys.modules', {'config': None}):
    import agent.storage
    import importlib
    importlib.reload(agent.storage)

from agent.storage import add_result, get_latest_results, get_results_by_endpoint, Session, Base, engine

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_add_and_retrieve_result(db_session):
    endpoint = "https://example.com"
    status_code = 200
    response_time = 0.5

    add_result(endpoint, status_code, response_time)

    results = get_latest_results()
    assert len(results) == 1
    assert results[0].endpoint == endpoint

    # Test exception rollback
    with patch('agent.storage.Session') as mock_session_maker:
        mock_sess = mock_session_maker.return_value
        mock_sess.commit.side_effect = Exception("DB Error")
        add_result(endpoint, status_code, response_time)
        mock_sess.rollback.assert_called_once()

def test_get_results_by_endpoint(db_session):
    endpoint1 = "https://example.com"
    add_result(endpoint1, 200, 0.5)
    add_result("https://google.com", 200, 0.6)
    add_result(endpoint1, 500, 0.1, error_message="Internal Server Error")

    assert len(get_results_by_endpoint(endpoint1)) == 2
    assert len(get_results_by_endpoint("https://google.com")) == 1
