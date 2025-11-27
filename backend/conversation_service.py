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
        # You can keep this in a file (e.g., prompts/aisle_master.txt)
        with open("prompts/aisle_master.txt", "r", encoding="utf-8") as f:
            self.master_prompt = f.read()

    def start_conversation(self, user_id=None):
        """
        Start a new conversation in the ONBOARDING state.
        Generate the first question: ask the user's Finnish language level.
        """

        # Auto-generate user_id if not provided
        if not user_id:
            user_id = str(uuid.uuid4())
            self.sessions.get_session(user_id)  # initialize session

        # Explicitly tell the AI it is in ONBOARDING state
        system_message = self.master_prompt + "\n\n" + \
            "You are now in the ONBOARDING state. " \
            "Generate the first question asking the user's Finnish language level (A0, A1, A2, B1). " \
            "End with a guiding question."

        messages = [
            {"role": "system", "content": system_message}
        ]

        # Call the AI model
        raw_output = self.llm.generate(messages)

        # Parse response
        json_output = parse_ai_response(raw_output)

        # Initialize session state and history
        self.sessions.set_state(user_id, json_output.get("state", "ONBOARDING"))
        self.sessions.update_history(user_id, "", json_output.get("finnish", ""))

        return user_id, json_output

    def handle_message(self, user_id, user_msg):
        """
        Handle user message:
        - Build AI prompt based on user state
        - Call model
        - Parse response
        - Validate
        - Update session
        """

        # Auto-generate user_id if not provided
        if not user_id:
            user_id = str(uuid.uuid4())
            self.sessions.get_session(user_id)  # initialize session

        # Get current state
        current_state = self.sessions.get_state(user_id)
        print(f"User {user_id} in state {current_state}")

        # Build message history for LLM
        messages = [
            {"role": "system", "content": self.master_prompt}
        ]

        # Add conversation history
        for entry in self.sessions.get_history(user_id):
            if entry["user"]:
                messages.append({"role": "user", "content": entry["user"]})
            if entry["ai"]:
                messages.append({"role": "assistant", "content": entry["ai"]})

        # Add current user message
        messages.append({"role": "user", "content": user_msg})

        # Call the AI model
        raw_output = self.llm.generate(messages)

        # Parse response
        json_output = parse_ai_response(raw_output)

        # Update session
        self.sessions.set_state(user_id, json_output.get("state", current_state))
        self.sessions.update_history(user_id, user_msg, json_output.get("finnish", ""))

        return json_output
