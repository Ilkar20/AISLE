# routes/chat_routes.py
from flask import Blueprint, request
from controllers.chat_controller import process_chat

chat_router = Blueprint("chat_router", __name__)
router = chat_router  # backwards-compatible alias

@chat_router.route("/chat", methods=["POST"])
def chat():
    """
    Receives a user message, returns AI response in JSON.
    Expected JSON payload: { "message": "...", "session_id": "..." }
    """
    data = request.get_json() or {}
    message = data.get("message")
    session_id = data.get("session_id", "session2")

    return process_chat(message, session_id)