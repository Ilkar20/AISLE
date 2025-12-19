# routes/audio_routes.py
from flask import Blueprint, request, jsonify
from controllers.audio_controller import process_audio

audio_router = Blueprint("audio_router", __name__)
router = audio_router  # backwards-compatible alias

@audio_router.route("/audio/upload", methods=["POST"])
def upload_audio():
    """
    Receives an audio file and session_id, returns transcription + AI response.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    session_id = request.form.get("session_id", "session2")

    try:
        result = process_audio(file, session_id)
        return jsonify(result)
    except Exception as e:
        from flask import current_app
        current_app.logger.exception("Audio processing failed")
        return jsonify({"error": str(e)}), 500
