import pytest
import sys
import os
import streamlit
from unittest.mock import Mock, patch

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@patch('streamlit.set_page_config')
@patch('streamlit.markdown')
@patch('streamlit.title')
@patch('streamlit.header')
@patch('streamlit.sidebar')
@patch('streamlit.columns')
@patch('streamlit.line_chart')
@patch('streamlit.warning')
@patch('streamlit.info')
@patch('streamlit.stop')
@patch('streamlit.rerun')
def test_dashboard_import(mock_rerun, mock_stop, mock_info, mock_warning, mock_line_chart, mock_columns, mock_sidebar, mock_header, mock_title, mock_markdown, mock_set_page_config):
    # Mock return values
    mock_sidebar.slider.return_value = 10
    mock_sidebar.button.return_value = False

    # Configure mock_rerun to raise SystemExit so we simulate stopping execution
    mock_rerun.side_effect = SystemExit

    # Mock database session
    with patch('agent.storage.sessionmaker') as mock_sessionmaker:
        mock_session = Mock()
        mock_sessionmaker.return_value = mock_session
        mock_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = []

        # Import dashboard
        try:
            import dashboard
        except SystemExit:
            pass

        # Verify basic calls
        mock_set_page_config.assert_called()
        mock_title.assert_called()
        # Check that warning was called because data is empty
        assert mock_warning.called or mock_info.called
        assert mock_rerun.called
