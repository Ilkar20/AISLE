import os
import json
import uuid
from llm.openrouter_client import OpenRouterClient
from session_manager import RedisSessionManager  
from utils.parser import parse_ai_response  

class ConversationService:
    def __init__(self):
        self.llm = OpenRouterClient()
        self.sessions = RedisSessionManager()

        # Load the master AISLE prompt once at initialization
        with open("prompts/aisle_master.txt", "r", encoding="utf-8") as f:
            self.master_prompt = f.read()

    def handle_message(self, user_msg=None):
        """
        Handle user message or bootstrap a new conversation:
        - If no history and no user_msg, generate the first onboarding question.
        - Otherwise, continue the conversation based on state and history.
        """

        # We only keep a single server-side session (no per-user ids)
        session_id = "default"
        self.sessions.get_session(session_id)  # initialize session (idempotent)

        # Get current state
        current_state = self.sessions.get_state(session_id)
        print(f"Session {session_id} in state {current_state}")

        # Build message history for LLM
        history = self.sessions.get_history(session_id)
        print(f"History for session {session_id}: {history}")

        # If no user message and no history → bootstrap first onboarding question
        if not history:
            bootstrap_instruction = (
                "You are now in the ONBOARDING state. "
                "Generate the first question asking the user's Finnish language level (A0, A1, A2, B1). "
                "End with a guiding question."
            )
            history.append({"role": "system", "content": self.master_prompt})
            history.append({"role": "user", "content": bootstrap_instruction})     
        else:
            # Add current user message if provided
            if user_msg:
                history.append({"role": "user", "content": user_msg})

        # Call the AI model
        raw_output = self.llm.generate(history)

        # Parse response
        json_output = parse_ai_response(raw_output)

        # Update session state (ignore empty/falsey states coming from LLM)
        new_state = json_output.get("state")
        if new_state != current_state:
            print(f"Updating state for session {session_id}: {current_state} -> {new_state}")
        self.sessions.set_state(session_id, new_state)

        # Update history
        self.sessions.update_history(session_id, user_msg, )

        # Return parsed AI output (no user_id) — single-session app
        return json_output
