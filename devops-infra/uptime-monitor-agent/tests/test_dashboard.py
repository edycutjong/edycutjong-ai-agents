import pytest
import sys
import os
import time
from unittest.mock import Mock, MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.storage import add_result, Base, engine, Session

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

class SessionState(dict):
    def __getattr__(self, name):
        return self.get(name)
    def __setattr__(self, name, value):
        self[name] = value

def run_dashboard_with_mock(monkeypatch, session_state=None, trigger_refresh=False):
    mock_st = MagicMock()
    mock_st.session_state = SessionState() if session_state is None else session_state
    
    if trigger_refresh:
        mock_st.session_state.last_refresh = time.time() - 1000
    
    mock_st.sidebar.slider.return_value = 10
    mock_st.sidebar.button.return_value = False
    
    class RerunException(Exception): pass
    class StopException(Exception): pass
    mock_st.rerun.side_effect = RerunException("Rerun")
    mock_st.stop.side_effect = StopException("Stop")
    
    mock_cols = [MagicMock() for _ in range(4)]
    for c in mock_cols:
        c.__enter__.return_value = c
    mock_st.columns.return_value = mock_cols
    
    mock_exp = MagicMock()
    mock_exp.__enter__.return_value = mock_exp
    mock_st.expander.return_value = mock_exp

    monkeypatch.setitem(sys.modules, "streamlit", mock_st)
    if 'dashboard' in sys.modules:
        del sys.modules['dashboard']
    
    return mock_st, RerunException, StopException

def test_dashboard_full(monkeypatch):
    add_result("http://test.com", 200, 0.1, None, 50, None)
    add_result("http://test.com", 500, 0.2, "err", 10, "diag")
    add_result("http://other.com", 500, 0.1, "err", None, None) # No AI diagnosis, no SSL
    
    mock_st, _, _ = run_dashboard_with_mock(monkeypatch)
    import dashboard
    assert mock_st.header.called

def test_dashboard_all_up(monkeypatch):
    add_result("http://test.com", 200, 0.1, None, None, None)
    mock_st, _, _ = run_dashboard_with_mock(monkeypatch)
    import dashboard
    mock_st.success.assert_called_with("No recent failures detected.")
    mock_st.info.assert_any_call("No SSL data available.")

def test_dashboard_empty(monkeypatch):
    mock_st, RerunException, StopException = run_dashboard_with_mock(monkeypatch)
    try:
        import dashboard
    except RerunException:
        pass
    mock_st.warning.assert_any_call("No monitoring data available yet. Please start the monitor agent: `python main.py`")

def test_dashboard_refresh_button(monkeypatch):
    mock_st, RerunException, StopException = run_dashboard_with_mock(monkeypatch)
    mock_st.sidebar.button.return_value = True
    try:
        import dashboard
    except RerunException:
        pass
    mock_st.sidebar.button.assert_called_with("Refresh Now")
    assert mock_st.rerun.called

def test_dashboard_refresh(monkeypatch):
    mock_st, RerunException, StopException = run_dashboard_with_mock(monkeypatch, trigger_refresh=True)
    try:
        import dashboard
    except RerunException:
        pass
    assert mock_st.rerun.called

def test_dashboard_missing_endpoint(monkeypatch):
    # If df isn't empty but is missing 'endpoint', which is practically impossible but we can mock it
    # Just to get full coverage
    add_result("http://test.com", 200, 0.1, None, 50, None)
    mock_st, RerunException, StopException = run_dashboard_with_mock(monkeypatch)
    
    with patch('pandas.DataFrame') as mock_df:
        mock_instance = MagicMock()
        mock_instance.empty = False
        mock_instance.columns = []
        mock_df.return_value = mock_instance
        try:
            import dashboard
        except RerunException:
            pass
        mock_st.warning.assert_any_call("No monitoring data available yet. Please start the monitor agent: `python main.py`")
        
def test_dashboard_no_unique_endpoints(monkeypatch):
    add_result("http://test.com", 200, 0.1, None, 50, None)
    mock_st, RerunException, StopException = run_dashboard_with_mock(monkeypatch)
    
    with patch('pandas.DataFrame') as mock_df:
        mock_instance = MagicMock()
        mock_instance.empty = False
        mock_instance.columns = ['endpoint']
        mock_instance['endpoint'].unique.return_value = []
        mock_df.return_value = mock_instance
        try:
            import dashboard
        except StopException:
            pass
        mock_st.warning.assert_any_call("No endpoints found in data.")
