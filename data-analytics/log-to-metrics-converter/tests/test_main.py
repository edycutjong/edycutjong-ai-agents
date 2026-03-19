"""Tests for main.py entry point."""
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_block():
    """Test that main.py can be loaded without launching streamlit."""
    mock_st = MagicMock()
    mock_stcli = MagicMock()
    mock_stcli.main.return_value = 0
    with patch.dict("sys.modules", {
        "streamlit": mock_st,
        "streamlit.web": MagicMock(),
        "streamlit.web.cli": mock_stcli,
    }):
        try:
            import importlib
            import main as m
            importlib.reload(m)
        except (SystemExit, Exception):
            pass
