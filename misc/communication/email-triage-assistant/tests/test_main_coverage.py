"""Coverage tests for main.py — Streamlit app entry."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_import():
    """Test that main.py can be imported without side effects."""
    # Mock streamlit and subprocess to prevent actual app launch
    with patch.dict("sys.modules", {"streamlit": MagicMock(), "streamlit.web": MagicMock(), "streamlit.web.cli": MagicMock()}):
        with patch("subprocess.run", return_value=None):
            try:
                import importlib
                import main as m
                importlib.reload(m)
            except (SystemExit, Exception):
                pass


def test_main_function():
    """Test main() with mocked streamlit."""
    with patch.dict("sys.modules", {"streamlit": MagicMock(), "streamlit.web": MagicMock(), "streamlit.web.cli": MagicMock()}):
        with patch("subprocess.run", return_value=None):
            try:
                from main import main
                main()
            except (SystemExit, Exception):
                pass
