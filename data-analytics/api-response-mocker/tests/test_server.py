import pytest
from fastapi.testclient import TestClient
from agent.server import MockServer
from agent.parser import OpenAPIParser
import os

@pytest.fixture
def parser():
    spec_path = os.path.join(os.path.dirname(__file__), 'sample_spec.yaml')
    with open(spec_path, 'r') as f:
        spec_content = f.read()
    return OpenAPIParser(spec_content)

@pytest.fixture
def client(parser):
    server = MockServer(parser)
    return TestClient(server.app)

def test_mock_server_routes(client):
    response = client.get("/users")
    if response.status_code != 200:
        print(response.text)  # pragma: no cover
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "id" in data[0]

def test_mock_server_path_params(client):
    response = client.get("/users/123")
    if response.status_code != 200:
        print(response.text)  # pragma: no cover
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data

def test_mock_server_latency(parser):
    # Set latency to 100ms
    config = {'latency_ms': 100}
    server = MockServer(parser, config)
    client = TestClient(server.app)

    import time
    start = time.time()
    client.get("/users")
    duration = (time.time() - start) * 1000
    assert duration >= 100

def test_mock_server_error_simulation(parser):
    # Set error rate to 100%
    config = {'error_rate': 1.0}
    server = MockServer(parser, config)
    client = TestClient(server.app)

    response = client.get("/users")
    assert response.status_code >= 400

def test_mock_server_update_config(parser):
    server = MockServer(parser)
    assert server.latency_ms == 0
    assert server.error_rate == 0.0
    server.update_config({'latency_ms': 50, 'error_rate': 0.5})
    assert server.latency_ms == 50
    assert server.error_rate == 0.5

def test_mock_server_no_schema():
    from agent.parser import OpenAPIParser
    spec = """
openapi: 3.0.0
info:
  title: Test
  version: 1.0.0
paths:
  /empty:
    get:
      responses:
        '200':
          description: OK
    """
    parser = OpenAPIParser(spec)
    server = MockServer(parser)
    client = TestClient(server.app)

    response = client.get("/empty")
    assert response.status_code == 200
    assert response.json() == {"message": "Success (no schema defined)"}
