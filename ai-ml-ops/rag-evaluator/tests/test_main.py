import os
import sys
import runpy
from io import StringIO
import pytest


import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_builtin_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "dummy")  # pragma: no cover


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

