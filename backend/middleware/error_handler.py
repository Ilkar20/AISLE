# middleware/error_handler.py
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # You can log the exception here if needed
        return jsonify({"error": str(e)}), 500
