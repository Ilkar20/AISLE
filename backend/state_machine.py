# backend/state_machine.py
"""
Deterministic state machine for the onboarding flow and simple transitions.
Keeps validation & parsing of user replies for onboarding.
"""

import re
from typing import Tuple, Optional

class StateMachine:
    """
    States:
      - onboarding_language
      - onboarding_sector
      - onboarding_level
      - theme_selection
      - situation_selection
      - lesson_start
      - exercise
      - feedback
      - dashboard
    """

    def consume(self, state: str, user_message: str, profile: dict) -> Tuple[str, dict]:
        """
        Given current state and user message, update profile accordingly and
        return (new_state, action).
        action is an optional dict with hints for prompt builder.
        """
        msg = (user_message or "").strip()
        action = {}

        # --- Language selection ---
        if state == "onboarding_language":
            if not msg:
                return state, {"ask": True}
            lang = self._parse_language(msg)
            if lang:
                profile["ui_lang"] = lang
                return "onboarding_sector", {"ask_sector": True}
            else:
                return state, {"invalid_lang": True}

        # --- Sector selection ---
        if state == "onboarding_sector":
            if not msg:
                return state, {"ask_sector": True}
            # Free-text sector for now; normalize
            profile["sector"] = msg
            return "onboarding_level", {"ask_level": True}

        # --- Level selection ---
        if state == "onboarding_level":
            if not msg:
                return state, {"ask_level": True}
            level = self._parse_level(msg)
            if level:
                profile["self_cefr"] = level
                # mark onboarded and award badge
                profile.setdefault("badges", [])
                if "Aloitit AISLEn" not in profile["badges"]:
                    profile["badges"].append("Aloitit AISLEn")
                profile["onboarded"] = True
                return "theme_selection", {"onboarding_complete": True}
            else:
                return state, {"invalid_level": True}
            
        # --- Theme selection ---
        if state == "situation_selection":
            if not msg:
                return state, {"ask_situation": True}
            profile["selected_situation"] = msg
            return "lesson_start", {"start _lesson": True}
        
        # --- Situation selection ---
        if state == "situation_selection":
            if not msg:
                return state, {"ask_situation": True}
            profile["selected_situation"] = msg
            return "lesson_start", {"start_lesson": True}
        
        # --- Lesson start ---
        if state == "lesson_start":
            return "exercise", {"start_exercise": True}
        
        # --- Exercise ---
        if state == "exercise":
            profile["last_points"] = 10
            return "feedback", {"give_feedback": True}
        
        # --- Feedback ---
        if state == "feedback":
            profile.setdefault("badges", [])
            if "First Exercise" not in profile["badges"]:
                profile["badges"].append("First Exercise")
            return "dashboard",  {"show-dashboard": True}
        
        # --- Dashboard ---
        if state == "dashboard":
            return state, {"dashboard_ready": True}
        

        # For other states, just keep them (later we'll add transitions)
        return state, {}

    def _parse_language(self, text: str) -> Optional[str]:
        t = text.lower()
        if "english" in t or t in ("en", "englanti", "englanti.", "englanti?"):
            return "en"
        if "suomi" in t or "finnish" in t or t in ("fi", "suomi.", "suomi?"):
            return "fi"
        # accept single-word codes too
        if t in ("en", "fi"):
            return t
        return None

    def _parse_level(self, text: str) -> Optional[str]:
        t = text.strip().upper()
        # Accept forms like "A1", "A2", "B1" or "A1 level"
        for code in ("A1", "A2", "B1"):
            if code in t:
                return code
        # also allow english words like 'beginner' -> map to A1
        if "beginner" in t:
            return "A1"
        return None
