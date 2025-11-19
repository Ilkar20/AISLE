class SessionManager:
    """
    Simple in-memory session manager.
    Tracks user state and conversation history.
    """

    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id):
        if user_id not in self.sessions:
            # Initialize new user session
            self.sessions[user_id] = {
                "state": "onboarding",
                "history": []
            }
        return self.sessions[user_id]

    def update_history(self, user_id, user_msg, ai_msg):
        session = self.get_session(user_id)
        session["history"].append({"user": user_msg, "ai": ai_msg})

    def set_state(self, user_id, state):
        session = self.get_session(user_id)
        session["state"] = state

    def get_state(self, user_id):
        return self.get_session(user_id)["state"]

    def get_history(self, user_id):
        return self.get_session(user_id)["history"]
