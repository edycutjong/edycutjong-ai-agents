import pytest
import sys
import os
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage

# Add parent dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock config
sys.modules["apps.agents.security_privacy.permission_auditor.config"] = MagicMock()
# Also mock local config import if needed, but since we modify sys.path...
# Let's just set the environment variable for the process to be safe
os.environ["OPENAI_API_KEY"] = "test-key"

from agent.core import PermissionAuditorAgent

@pytest.fixture
def mock_agent():
    with patch("agent.core.ChatOpenAI") as mock_llm_cls:
        # Configure the mock class to return a mock instance
        mock_llm_instance = MagicMock()
        mock_llm_cls.return_value = mock_llm_instance

        # Instantiate agent
        agent = PermissionAuditorAgent()

        # We need to mock the invoke method on the instance
        agent.llm.invoke = MagicMock()

        return agent

def test_parse_manifest_file(mock_agent):
    # This doesn't use LLM, just parsers
    # We need to mock the parser result or check if real parser is called.
    # The agent calls real parsers.

    # We can mock identify_file_type and parse_android_manifest if we want isolated unit test,
    # but using real parsers here is fine as integration test for agent->parser connection.

    content = """
    <manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.app">
        <uses-permission android:name="android.permission.CAMERA" />
    </manifest>
    """
    permissions, platform = mock_agent.parse_manifest_file(content, "AndroidManifest.xml")
    assert platform == "android"
    assert "android.permission.CAMERA" in permissions

def test_analyze_permissions(mock_agent):
    permissions = ["android.permission.CAMERA"]
    description = "A camera app"
    platform = "android"

    mock_response_content = '{"risk_level": "Low", "summary": "Safe", "analysis": []}'

    # Mock LLM response. Since llm is not a Runnable, LangChain wraps it as RunnableLambda
    # which calls the object (__call__), not .invoke()
    mock_agent.llm.return_value = AIMessage(content=mock_response_content)

    result = mock_agent.analyze_permissions(permissions, description, platform)

    assert mock_agent.llm.called
    assert result["risk_level"] == "Low"

def test_generate_justification(mock_agent):
    permissions = ["android.permission.CAMERA"]
    description = "A camera app"

    mock_agent.llm.return_value = AIMessage(content="# Justification\n\nCamera is needed.")

    result = mock_agent.generate_justification(permissions, description)

    assert mock_agent.llm.called
    assert "Camera is needed" in result
