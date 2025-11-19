# router.py
from flask import Blueprint, request, jsonify
from conversation_service import generate_ai_response
from session_manager import create_session, get_session, update_session

bp = Blueprint("aisle_bp", __name__)

@bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    message = data.get("message", "")

    # Create session if none
    if not session_id:
        session_id = create_session()

    session = get_session(session_id)

    # Generate AI prompt (simplified)
    prompt = f"User state: {session['state']}. User says: {message}"

    ai_reply = generate_ai_response(prompt, session_id)

    # Update session (example: advance state if onboarding done)
    if session['state'] == "onboarding":
        session['state'] = "theme_selection"

    update_session(session_id, session)

    return jsonify({
        "session_id": session_id,
        "state": session['state'],
        "reply": ai_reply
    })
