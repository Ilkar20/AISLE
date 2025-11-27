import json
import redis
import os
from dotenv import load_dotenv

load_dotenv()  # loads environment variables from .env

class RedisSessionManager:
    """
    Session manager using Redis.
    Stores state and conversation history.
    Single-session only (no user_id required).
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
        self.SESSION_KEY = "session:default"

    def get_session(self):
        raw = self.redis.get(self.SESSION_KEY)
        if raw:
            return json.loads(raw)

        # initialize with canonical uppercase state
        session = {"state": "ONBOARDING", "history": []}
        self.redis.set(self.SESSION_KEY, json.dumps(session, ensure_ascii=False), ex=self.SESSION_TTL)
        return session

    def save_session(self, session):
        self.redis.set(self.SESSION_KEY, json.dumps(session, ensure_ascii=False), ex=self.SESSION_TTL)

    def update_history(self, user_msg=None, ai_msg=None):
        session = self.get_session()
        session["history"].append({"user": user_msg, "ai": ai_msg})
        self.save_session(session)

    def set_state(self, state):
        session = self.get_session()
        if state:
            session["state"] = state.upper()
        else:
            session["state"] = session.get("state", "ONBOARDING")
        self.save_session(session)

    def get_state(self):
        return self.get_session()["state"]

    def get_history(self):
        return self.get_session()["history"]
