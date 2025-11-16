# backend/session_manager.py
import uuid
import time
from typing import Dict

class SessionManager:
    """
    Simple in-memory session manager.
    Replace with Redis or DB for production.
    """
    def __init__(self):
        self._store: Dict[str, dict] = {}

    def create_session(self):
        sid = str(uuid.uuid4())
        now = time.time()
        self._store[sid] = {
            "state": "onboarding_language",
            "created_at": now,
            "last_active": now,
            "history": [],  # list of dicts {role:'user'|'assistant', text: {'fi','en'}}
            "profile": {},  # ui_lang, sector, self_cefr, badges, xp, etc.
        }
        return sid

    def exists(self, sid: str) -> bool:
        return sid in self._store

    def touch(self, sid: str):
        if sid in self._store:
            self._store[sid]["last_active"] = time.time()

    def get_state(self, sid: str) -> str:
        return self._store[sid]["state"]

    def set_state(self, sid: str, state: str):
        self._store[sid]["state"] = state
        self.touch(sid)

    def append_history(self, sid: str, role: str, text, audio, image, video):
        entry = {
            "role": role, 
            "text": text,
            "audio": audio,
            "image": image,
            "video": video, 
            "ts": time.time(),
            }
        self._store[sid]["history"].append(entry)
        self.touch(sid)

    def get_history(self, sid: str):
        return self._store[sid]["history"]

    def get_profile(self, sid: str):
        return self._store[sid]["profile"]

    def set_profile(self, sid: str, profile: dict):
        self._store[sid]["profile"] = profile
        self.touch(sid)

    def set_profile_field(self, sid: str, key: str, value):
        self._store[sid]["profile"][key] = value
        self.touch(sid)

    def delete_session(self, sid: str):
        if sid in self._store:
            del self._store[sid]
