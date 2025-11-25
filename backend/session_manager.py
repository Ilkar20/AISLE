import json
import redis
import os
from dotenv import load_dotenv

load_dotenv()  # loads environment variables from .env

class RedisSessionManager:
    """
    Session manager using Redis.
    Stores state and conversation history.
    """

    def __init__(self):
        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            username=os.getenv("REDIS_USERNAME"),
            password=os.getenv("REDIS_PASSWORD"),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,  # ensures ä, ö, å display correctly
        )
        self.SESSION_TTL = int(os.getenv("SESSION_TTL", 86400))  # default 24h

    def _session_key(self, user_id):
        return f"session:{user_id}"

    def get_session(self, user_id):
        key = self._session_key(user_id)
        raw = self.redis.get(key)

        if raw:
            return json.loads(raw)

        session = {"state": "onboarding", "history": []}
        self.redis.set(key, json.dumps(session, ensure_ascii=False), ex=self.SESSION_TTL)
        return session

    def save_session(self, user_id, session):
        key = self._session_key(user_id)
        self.redis.set(key, json.dumps(session, ensure_ascii=False), ex=self.SESSION_TTL)

    def update_history(self, user_id, user_msg, ai_msg):
        session = self.get_session(user_id)
        session["history"].append({"user": user_msg, "ai": ai_msg})
        self.save_session(user_id, session)

    def set_state(self, user_id, state):
        session = self.get_session(user_id)
        session["state"] = state
        self.save_session(user_id, session)

    def get_state(self, user_id):
        return self.get_session(user_id)["state"]

    def get_history(self, user_id):
        return self.get_session(user_id)["history"]
