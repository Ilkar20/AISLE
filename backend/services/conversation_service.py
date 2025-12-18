from llm.openrouter_client import OpenRouterClient
from session_manager import RedisSessionManager
from utils.parser import parse_ai_response

class ConversationService:
    def __init__(self, session_id):
        """
        ConversationService requires an explicit session_id.
        """
        self.llm = OpenRouterClient()
        self.sessions = RedisSessionManager(session_id)

        existing = self.sessions.get_session()
        if not existing or "memory" not in existing:
            self.sessions.init_session()

    def handle_message(self, user_msg=None):
        """
        Handle user message or bootstrap a new conversation:
        - If no history and no user_msg, generate the first onboarding question.
        - Otherwise, continue the conversation based on history.
        """
        session = self.sessions.get_session()
        memory = session.get("memory", [])
        print(f"History for session {self.sessions.session_id}: {memory}")

        # Global schema enforcement instruction
        schema_instruction = (
            "You are AISLE, a Finnish tutor. Always respond ONLY in JSON with keys: "
            "{'english': <English reply>, 'finnish': <Finnish reply>, 'state': <FSM state>}."
            " End with a guiding question."
        )

        # Bootstrap if empty
        if not memory:
            first_question = (
                "You are now in the ONBOARDING phase. "
                "Generate the first question asking the user's Finnish language level (A0, A1, A2, B1). "
            )
            memory.append({"role": "system", "content": first_question})
            memory.append({"role": "system", "content": schema_instruction})
        elif user_msg and user_msg.strip():
            # Append user message cleanly
            memory.append({"role": "user", "content": user_msg.strip()})
            # Reinforce schema instruction separately
            memory.append({"role": "system", "content": schema_instruction})

        print(f"Sending to LLM for session {self.sessions.session_id}: {memory}")
        raw_output = self.llm.generate(memory)
        print(f"Raw LLM output for session {self.sessions.session_id}: {raw_output}")

        # Parse response
        json_output = parse_ai_response(raw_output)
        print(f"LLM output for session {self.sessions.session_id}: {json_output}")

        # Append assistant reply to memory
        ai_response = json_output.get("english")
        if ai_response:
            memory.append({"role": "assistant", "content": ai_response})

        # Save updated session back to Redis
        session["memory"] = memory
        self.sessions.save_session(session)

        # Return parsed AI output
        return json_output
