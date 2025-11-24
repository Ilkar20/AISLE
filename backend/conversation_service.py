import os
import json
from llm.openrouter_client import OpenRouterClient
from prompt_manager import PromptManager
from session_manager import SessionManager
from utils.parser import parse_ai_response  

class ConversationService:
    def __init__(self):
        self.llm = OpenRouterClient()
        self.prompts = PromptManager()
        self.sessions = SessionManager()

    
    def handle_message(self, user_id, user_msg):
        """
        Handle user message:
        - Build AI prompt based on user state
        - Call model
        - Parse response
        - Validate
        - Update session
        """
        # Get current state
        current_state = self.sessions.get_state(user_id)

        # Load prompts
        system_prompt = self.prompt_manager.get_system_prompt()
        state_prompt = self.prompt_manager.get_state_prompt(current_state)

        # Build message history for LLM
        messages = [
            {"role": "system", "content": system_prompt + "\n\n" + state_prompt}
        ]

        # Add conversation history
        for entry in self.sessions.get_history(user_id):
            messages.append({"role": "user", "content": entry["user"]})
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