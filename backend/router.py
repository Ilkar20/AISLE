# backend/router.py
from flask import Blueprint, request, jsonify
from conversation_service import ConversationService
from session_manager import SessionManager

bp = Blueprint("aisle", __name__)
session_mgr = SessionManager()
conv_service = ConversationService()

@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    message = data.get("message", "").strip()

    # create session if missing
    if not session_id:
        session_id = session_mgr.create_session()
        # initial assistant prompt (no user message)
        res = conv_service.handle_message(session_id, "", session_mgr)
        return jsonify(res)

    if not session_mgr.exists(session_id):
        return jsonify({"error":"invalid session_id"}), 400

    # append user msg
    if message:
        session_mgr.append_history(session_id, "user", {"fi": message, "en": message})

    res = conv_service.handle_message(session_id, message, session_mgr)
    return jsonify(res)

@bp.route("/state/<session_id>", methods=["GET"])
def get_state(session_id):
    """
    Get current state and profile for a session.
    """
    if not session_mgr.exists(session_id):
        return jsonify({"error": "invalid  session_id"}), 400
    return jsonify({
        "state": session_mgr.get_state(session_id),
        "profile": session_mgr.get_profile(session_id)
    }), 200

@bp.route("/history/<session_id>", method=["Get"])
def get_history(session_id):
    """
    Get full conversation history (multimodal entires).
    """
    if not session_mgr.exists(session_id):
        return jsonify({"error": "invalid session_id"}), 400
    return jsonify(session_mgr.get_history(session_id)), 200

@bp.route("/session/<session_id>", method=["DELETE"])
def delete_session(session_id):
    """
    Delete a session completely.
    """
    if not session_mgr.exists(session_id):
        return jsonify({"error": "invalid session_id"}), 400
    session_mgr.delete_session(session_id)
    return jsonify({"delete": session_id}), 200