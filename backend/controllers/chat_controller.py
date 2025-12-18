# controllers/chat_controller.py
import json
from flask import Response
from conversation_service import ConversationService

def process_chat(message: str, session_id: str = "session2") -> Response:
    """
    Controller for handling chat messages.
    - Calls ConversationService
    - Returns JSON Response
    """
    service = ConversationService(session_id)
    response = service.handle_message(message)

    payload = json.dumps(response, ensure_ascii=False)
    return Response(payload, mimetype="application/json; charset=utf-8")
