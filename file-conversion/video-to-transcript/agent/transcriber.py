import os
from openai import OpenAI

class Transcriber:
    def __init__(self, api_key: str):
        if not api_key:
             raise ValueError("API Key is required for Transcriber")
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, audio_path: str, response_format: str = "text", language: str = None):
        """
        Transcribes audio file using OpenAI Whisper API.

        Args:
            audio_path (str): Path to the audio file.
            response_format (str): Desired format ('json', 'text', 'srt', 'verbose_json', 'vtt').
            language (str): ISO-639-1 language code (optional).

        Returns:
            str or dict: The transcription result.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format=response_format,
                    language=language
                )
            return transcript
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")
