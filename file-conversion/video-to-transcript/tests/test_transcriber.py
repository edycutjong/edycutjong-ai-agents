import pytest
from unittest.mock import MagicMock, patch, mock_open
import os
import sys

# Add app directory to path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from agent.transcriber import Transcriber

@patch("agent.transcriber.OpenAI")
def test_transcribe_success(mock_openai):
    # Setup mock
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.audio.transcriptions.create.return_value = "This is a transcript."

    transcriber = Transcriber(api_key="test_key")

    audio_path = "test_audio.mp3"
    with open(audio_path, "w") as f:
        f.write("dummy")

    try:
        result = transcriber.transcribe(audio_path)

        # Assertions
        mock_client.audio.transcriptions.create.assert_called_once()
        assert result == "This is a transcript."

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

def test_transcriber_no_api_key():
    with pytest.raises(ValueError):
        Transcriber(api_key="")

def test_transcribe_file_not_found():
    # Mock OpenAI init to avoid needing valid key or connection
    with patch("agent.transcriber.OpenAI"):
        transcriber = Transcriber(api_key="test_key")
        with pytest.raises(FileNotFoundError):
            transcriber.transcribe("non_existent.mp3")
