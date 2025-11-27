from flask import Blueprint, request, jsonify, Response
import json
from conversation_service import ConversationService

chat_router = Blueprint("chat_router", __name__)
# Backwards-compatible name used by app.py so app.register_blueprint(router) works
router = chat_router
conversation_service = ConversationService()

@chat_router.route("/chat", methods=["POST"])
def chat():
    """
    Receives a user message, returns AI response in JSON.
    Expected JSON payload: { "message": "..." }
    Note: single-session mode — no user_id required.
    """
    data = request.get_json() or {}
    message = data.get("message")

    response = conversation_service.handle_message(message)
    # Use ensure_ascii=False to preserve non-ascii characters (ä, ö, å) in output
    payload = json.dumps(response, ensure_ascii=False)
    return Response(payload, mimetype="application/json; charset=utf-8")
