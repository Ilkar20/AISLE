# services/transcription_service.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio file using Whisper.
    """
    with open(file_path, "rb") as audio_file:
        result = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return result.text
