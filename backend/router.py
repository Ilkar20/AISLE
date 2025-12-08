from flask import Blueprint, request, jsonify, Response
import json
from conversation_service import ConversationService

chat_router = Blueprint("chat_router", __name__)
# Backwards-compatible name used by app.py so app.register_blueprint(router) works
router = chat_router

@chat_router.route("/chat", methods=["POST"])
def chat():
    """
    Receives a user message, returns AI response in JSON.
    Expected JSON payload: { "message": "..." }
    Note: single-session mode — no user_id required.
    """
    data = request.get_json() or {}
    message = data.get("message")
    session_id = data.get("session_id", "test1")

    service = ConversationService(session_id)
    response = service.handle_message(message)

    payload = json.dumps(response, ensure_ascii=False)
    return Response(payload, mimetype="application/json; charset=utf-8")
