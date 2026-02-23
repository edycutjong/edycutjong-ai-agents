import pytest
import os
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.storage import add_result, get_latest_results, get_results_by_endpoint, Session, Base, engine

@pytest.fixture(scope="function")
def db_session():
    # Setup: Create tables
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    # Teardown: Drop tables
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
    assert results[0].status_code == status_code
    assert results[0].response_time == response_time

def test_get_results_by_endpoint(db_session):
    endpoint1 = "https://example.com"
    endpoint2 = "https://google.com"

    add_result(endpoint1, 200, 0.5)
    add_result(endpoint2, 200, 0.6)
    add_result(endpoint1, 500, 0.1, error_message="Internal Server Error")

    results1 = get_results_by_endpoint(endpoint1)
    assert len(results1) == 2
    assert results1[0].endpoint == endpoint1
    assert results1[1].endpoint == endpoint1

    results2 = get_results_by_endpoint(endpoint2)
    assert len(results2) == 1
    assert results2[0].endpoint == endpoint2
