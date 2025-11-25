import os
import json
import uuid
from llm.openrouter_client import OpenRouterClient
from prompt_manager import PromptManager
from session_manager import RedisSessionManager  
from utils.parser import parse_ai_response  

class ConversationService:
    def __init__(self):
        self.llm = OpenRouterClient()
        # canonical attribute name used elsewhere in code
        self.prompt_manager = PromptManager()
        # keep the older `prompts` name for backwards compatibility
        self.prompts = self.prompt_manager
        self.sessions = RedisSessionManager()

    
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

        # Load prompts
        system_prompt = self.prompt_manager.get_system_prompt()
        state_prompt = self.prompt_manager.get_state_prompt(current_state)

        # Build message history for LLM
        messages = [
            {"role": "system", "content": system_prompt + "\n\n" + state_prompt}
        ]

        print(f"System prompt for state {current_state}:\n{system_prompt}\n\n{state_prompt}")

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