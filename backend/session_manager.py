import json
import redis
import os
from dotenv import load_dotenv

load_dotenv()

class RedisSessionManager:
    """
    Session manager using Redis.
    Stores ephemeral conversation history.
    Requires explicit session_id so you can reconnect to the same session.
    """

    def __init__(self, session_id):
        if not session_id:
            raise ValueError("session_id must be provided explicitly")

        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            username=os.getenv("REDIS_USERNAME"),
            password=os.getenv("REDIS_PASSWORD"),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
        )
        self.SESSION_TTL = int(os.getenv("SESSION_TTL", 86400))  # default 24h
        self.session_id = session_id
        self.SESSION_KEY = f"aisle:session:{self.session_id}"

    def init_session(self):
        """Initialize a new session with empty memory."""
        session = {"memory": []}
        self.redis.set(
            self.SESSION_KEY,
            json.dumps(session, ensure_ascii=False),
            ex=self.SESSION_TTL
        )
        return session

    def get_session(self):
        """Retrieve session object, initialize if missing."""
        raw = self.redis.get(self.SESSION_KEY)
        if raw:
            return json.loads(raw)
        return self.init_session()

    def save_session(self, session):
        """Persist session object back to Redis."""
        self.redis.set(
            self.SESSION_KEY,
            json.dumps(session, ensure_ascii=False),
            ex=self.SESSION_TTL
        )
