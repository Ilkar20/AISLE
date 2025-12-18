# app.py
import os
from flask import Flask
from flask_cors import CORS

# Import your blueprints
from routes.chat_routes import chat_router
from routes.audio_routes import audio_router

# Optional middleware imports
from middleware.error_handler import register_error_handlers
from middleware.logging import setup_logging

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(chat_router, url_prefix="/api")
    app.register_blueprint(audio_router, url_prefix="/api")

    # Register middleware
    register_error_handlers(app)
    setup_logging(app)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    print(f"AISLE backend running at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
s