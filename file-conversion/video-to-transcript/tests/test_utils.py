import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add app directory to path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from agent.utils import extract_audio

@patch("agent.utils.VideoFileClip")
def test_extract_audio_success(mock_video_clip):
    # Setup mock
    mock_clip_instance = MagicMock()
    mock_video_clip.return_value = mock_clip_instance
    mock_audio = MagicMock()
    mock_clip_instance.audio = mock_audio

    video_path = "test_video.mp4"
    output_path = "test_audio.mp3"

    # Create dummy video file
    with open(video_path, "w") as f:
        f.write("dummy")

    try:
        result = extract_audio(video_path, output_path)

        # Assertions
        mock_video_clip.assert_called_once_with(video_path)
        mock_audio.write_audiofile.assert_called_once_with(output_path, codec='mp3', verbose=False, logger=None)
        assert result == output_path

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

def test_extract_audio_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract_audio("non_existent.mp4", "output.mp3")

def test_extract_audio_already_audio():
    audio_path = "test_audio.mp3"
    # Create dummy audio file
    with open(audio_path, "w") as f:
        f.write("dummy")

    try:
        result = extract_audio(audio_path, "output.mp3")
        assert result == audio_path
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
