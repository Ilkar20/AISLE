# app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from routes.chat_routes import chat_router
from routes.audio_routes import audio_router
from middleware.error_handler import register_error_handlers


def create_app():
    # Load environment variables from backend/.env
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Info log on startup
    app.logger.info("AISLE backend starting with Local Whisper transcription enabled.")

    # Register blueprints
    app.register_blueprint(chat_router, url_prefix="/api")
    app.register_blueprint(audio_router, url_prefix="/api")

    # Register middleware
    register_error_handlers(app)

    # Health check route
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "transcription": "local_whisper",  # explicitly show transcription mode
        })

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    print(f"AISLE backend running at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
