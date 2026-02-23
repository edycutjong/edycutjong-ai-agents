import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import agent.run_server

def test_run_server_function():
    with patch('agent.run_server.uvicorn.run') as mock_run:
        with patch('agent.run_server.OpenAPIParser') as MockParser:
            mock_parser_instance = MockParser.return_value
            mock_parser_instance.specification = {'info': {'title': 'Test'}}
            mock_parser_instance.get_paths.return_value = []

            with patch('builtins.open', create=True) as mock_open:
                mock_file = MagicMock()
                mock_file.read.return_value = "openapi: 3.0.0"
                mock_open.return_value.__enter__.return_value = mock_file

                with patch('agent.run_server.MockServer') as MockServer:
                    mock_server_instance = MockServer.return_value
                    mock_server_instance.app = MagicMock()

                    # Test logic
                    agent.run_server.run("spec.yaml", 8000, 0, 0.0, "log.json")

                    mock_run.assert_called_once()
                    assert mock_run.call_args[0][0] == mock_server_instance.app
                    assert mock_run.call_args[1]['port'] == 8000
