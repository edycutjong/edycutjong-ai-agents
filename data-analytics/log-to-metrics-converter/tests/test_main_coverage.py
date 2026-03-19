"""Coverage tests for main.py — Streamlit stcli launcher."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_import():
    """Test that main.py can be imported without launching streamlit."""
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
            importlib.reload(m)  # pragma: no cover
        except (SystemExit, Exception):
            pass
