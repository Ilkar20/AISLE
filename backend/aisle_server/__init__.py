from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow frontend requests

    # Import and register routes
    from .routes.onboarding import bp as onboarding_bp
    app.register_blueprint(onboarding_bp, url_prefix="/onboard")

    return app
