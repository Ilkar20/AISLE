from flask import Blueprint, jsonify, request

bp = Blueprint("onboarding", __name__)

@bp.route("/create", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username", "Guest")
    language = data.get("language", "fi")
    
    # Mock user creation
    user = {
        "user_id": 1,
        "username": username,
        "language": language
    }
    return jsonify({"success": True, "user": user})
