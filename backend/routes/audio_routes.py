# routes/audio_routes.py
import os
from flask import Blueprint, request, jsonify, current_app
from controllers.audio_controller import process_audio

audio_router = Blueprint("audio_router", __name__)
router = audio_router  # backwards-compatible alias

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@audio_router.route("/audio/upload", methods=["POST"])
def upload_audio():
    """
    Receives an audio file and session_id, saves file, returns transcription + AI response.
    Expected multipart/form-data payload:
      - file: audio file
      - session_id: optional, defaults to "session2"
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    # Use a truthy fallback so empty string values don't bypass the default.
    session_id = request.form.get("session_id") or "session2"

    # Save uploaded file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        file.save(file_path)
    except Exception as e:
        current_app.logger.exception("Failed to save uploaded file")
        return jsonify({"error": f"File save failed: {e}"}), 500

    try:
        # Pass the saved file path (string) + session_id to controller
        result = process_audio(file_path, session_id)
        return jsonify(result)
    except Exception as e:
        current_app.logger.exception("Audio processing failed")
        return jsonify({"error": str(e)}), 500


@audio_router.route("/health", methods=["GET"])
def health():
    """Basic health-check endpoint for diagnostics."""
    return jsonify({"status": "ok"}), 200
