# backend/conversation_service.py
import os
from typing import Dict
from pathlib import Path
import json

from config import PROMPT_TEMPLATES_PATH
from state_machine import StateMachine

# lightweight LLM adapter: mock now, pluggable later
class LLMMockAdapter:
    def generate(self, template_text: str, context: Dict) -> Dict:
        """
        Very simple renderer: Not a real LLM. We use template control keywords in template files
        and return bilingual dicts {"fi": "...", "en": "..."}.
        """
        # naive substitution for placeholders in braces {key}
        result_text = template_text
        for k, v in context.items():
            result_text = result_text.replace("{{" + k + "}}", str(v))
            result_text = result_text.replace("{" + k + "}", str(v))
        # extract FI and EN lines
        fi_lines = []
        en_lines = []
        for line in result_text.splitlines():
            line = line.strip()
            if line.startswith("FI:"):
                fi_lines.append(line[3:].strip().strip('"'))
            elif line.startswith("EN:"):
                en_lines.append(line[3:].strip().strip('"'))
            # some templates include explicit blocks
            elif line.startswith("If step"):
                continue
        fi = " ".join(fi_lines).strip() or result_text
        en = " ".join(en_lines).strip() or result_text
        return {"fi": fi, "en": en}

class ConversationService:
    def __init__(self, templates_path: str = PROMPT_TEMPLATES_PATH):
        self.templates_path = Path(templates_path)
        self.state_machine = StateMachine()
        self.llm = LLMMockAdapter()

    def _load_template(self, name: str) -> str:
        path = self.templates_path / name
        if path.exists():
            return path.read_text(encoding="utf-8")
        # fallback minimal defaults
        defaults = {
            "onboarding_prompt.txt": "FI: 'Hello FI' \nEN: 'Hello EN'",
            "theme_prompt.txt": "FI: 'Valitse teema' \nEN: 'Choose theme'",
        }
        return defaults.get(name, "FI: '...'\nEN: '...'")

    def handle_message(self, session_id: str, user_message: str, session_mgr):
        """
        Main entry point called by router. It:
          - fetches current state
          - passes user_message to state_machine.consume which updates profile & state
          - loads the prompt template for the new state and calls LLM adapter
          - returns structured response
        """
        state = session_mgr.get_state(session_id)
        profile = session_mgr.get_profile(session_id)

        new_state, action = self.state_machine.consume(state, user_message, profile)
        session_mgr.set_state(session_id, new_state)
        session_mgr.set_profile(session_id, profile)

        # choose template name by new_state
        template_map = {
            "onboarding_language": "onboarding_prompt.txt",
            "onboarding_sector": "onboarding_prompt.txt",
            "onboarding_level": "onboarding_prompt.txt",
            "theme_selection": "theme_prompt.txt",
            "situation_selection": "situation_prompt.txt",
            "lesson_start": "exercise_prompt.txt",
            "exercise": "exercise_prompt.txt",
            "feedback": "feedback_prompt.txt",
            "dashboard": "dashboard_prompt.txt",
        }
        template_file = template_map.get(new_state, "onboarding_prompt.txt")
        template_text = self._load_template(template_file)

        context = {
            "step": new_state,
            "profile": json.dumps(profile),
            "theme": profile.get("selected_theme", ""),
            "points": profile.get("last_points", 0),
            "badge": (profile.get("badges") or [])[-1] if profile.get("badges") else ""
        }

        # generate reply using LLM adapter
        reply = self.llm.generate(template_text, context)

        # store reply into session history
        session_mgr.append_history(session_id, "assistant", reply)
        return {
            "session_id": session_id,
            "state": new_state,
            "reply": reply,
            "profile": profile,
            "action": action
        }
