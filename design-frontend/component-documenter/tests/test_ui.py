import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Ensure the parent directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Mock streamlit before importing main
sys.modules["streamlit"] = MagicMock()

from main import main

@patch("main.st")
@patch("main.ComponentDocumenter")
@patch("main.parse_uploaded_file")
def test_main_no_upload(mock_parse, mock_documenter, mock_st):
    # Setup mock
    mock_st.file_uploader.return_value = []

    main()

    # Verify basics
    mock_st.title.assert_called()
    mock_st.info.assert_any_call("Please upload one or more component files to get started.")

@patch("main.st")
@patch("main.ComponentDocumenter")
@patch("main.parse_uploaded_file")
def test_main_with_upload(mock_parse, mock_documenter, mock_st):
    # Setup mock
    mock_file = MagicMock()
    mock_file.name = "Test.tsx"
    mock_st.file_uploader.return_value = [mock_file]

    mock_parse.return_value = ("code", "react-ts")

    # Mock session state
    mock_st.session_state = {}

    # Mock button click to return True
    mock_st.button.return_value = True

    # Mock API Key input
    mock_st.text_input.return_value = "sk-test"

    # Mock Documenter
    mock_doc_instance = mock_documenter.return_value
    mock_doc_instance.generate_documentation.return_value = "Generated Docs"

    # Mock columns to return 2 items
    mock_col1 = MagicMock()
    mock_col2 = MagicMock()
    mock_st.columns.return_value = [mock_col1, mock_col2]

    # Mock context managers for columns
    mock_col1.__enter__.return_value = mock_col1
    mock_col1.__exit__.return_value = None
    mock_col2.__enter__.return_value = mock_col2
    mock_col2.__exit__.return_value = None

    main()

    # Verify interaction
    mock_parse.assert_called_with(mock_file)
    mock_documenter.assert_called_with(api_key="sk-test")
    mock_doc_instance.generate_documentation.assert_called_with("code", "react-ts")
    # Using 'in' operator on mock object for "docs_Test.tsx" in st.session_state
    # This is tricky with mocks. The code does: st.session_state[key] = val
    # Check if we stored it
    assert "docs_Test.tsx" in mock_st.session_state
    assert mock_st.session_state["docs_Test.tsx"] == "Generated Docs"
