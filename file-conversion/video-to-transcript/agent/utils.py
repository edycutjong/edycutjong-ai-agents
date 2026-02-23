import os
from moviepy import VideoFileClip

def extract_audio(video_path: str, output_path: str) -> str:
    """
    Extracts audio from a video file and saves it to output_path.
    If the input is already an audio file supported by Whisper, returns the path.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File not found: {video_path}")

    ext = os.path.splitext(video_path)[1].lower()
    supported_audio = ['.mp3', '.wav', '.m4a', '.flac', '.mpga', '.webm']

    if ext in supported_audio:
        return video_path

    try:
        # Load video
        video = VideoFileClip(video_path)

        # Extract audio
        if video.audio is None:
             raise RuntimeError("Video has no audio track.")

        video.audio.write_audiofile(output_path, codec='mp3', verbose=False, logger=None)

        # Close to release resources
        video.close()

        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to extract audio: {str(e)}")
