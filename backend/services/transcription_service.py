# services/transcription_service.py
import os
import platform
import logging

# --- Fix PyTorch DLL loading issue on Windows ---
if platform.system() == "Windows":
    import ctypes
    from importlib.util import find_spec
    try:
        if (spec := find_spec("torch")) and spec.origin and os.path.exists(
            dll_path := os.path.join(os.path.dirname(spec.origin), "lib", "c10.dll")
        ):
            ctypes.CDLL(os.path.normpath(dll_path))
    except Exception:
        pass

# --- Safe to import Whisper now ---
import whisper
import shutil

logger = logging.getLogger(__name__)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio using local Whisper model.
    Runs entirely offline, free of API quota limits.
    """

    # Normalize and validate path
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        return "⚠️ Audio file not found."

    # Whisper relies on ffmpeg being available on PATH for audio decoding
    if shutil.which("ffmpeg") is None:
        logger.error("ffmpeg not found in PATH; transcription requires ffmpeg")
        return (
            "⚠️ Transcription failed: 'ffmpeg' executable not found. "
            "Install ffmpeg and ensure it's on your PATH (e.g., via Chocolatey: `choco install ffmpeg` or Winget).")

    try:
        # Load a small model for speed; use "small"/"medium"/"large" for better accuracy
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        return result.get("text", "")
    except Exception as e:
        logger.error(f"Local Whisper transcription failed: {e}")
        return f"⚠️ Transcription failed: {e}"
