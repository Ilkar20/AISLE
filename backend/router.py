from flask import Blueprint, request, jsonify
from conversation_service import ConversationService

chat_router = Blueprint("chat_router", __name__)
conversation_service = ConversationService()

@chat_router.route("/chat", methods=["POST"])
def chat():
    """
    Receives a user message, returns AI response in JSON.
    Expected JSON payload: { "user_id": "...", "message": "..." }
    """
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    response = conversation_service.handle_message(user_id, message)
    return jsonify(response)
