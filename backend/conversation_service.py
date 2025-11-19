from llm.openrouter_client import OpenRouterClient
from prompt_manager import PromptManager

class ConversationService:
    """
    Handles the AISLE conversation with the user.
    Current scope: Onboarding phase only.

    Features:
    - Sends an introduction automatically on first access.
    - Asks first onboarding question without user input.
    - Maintains multi-turn conversation if history is provided.
    """

    def __init__(self):
        self.llm = OpenRouterClient()
        self.prompts = PromptManager()

    def onboarding(self, user_message: str = None, history=None):
        """
        Run one onboarding turn.

        Args:
            user_message (str, optional): User's message. If None, triggers intro + first question.
            history (list, optional): List of previous conversation turns (user + AI)

        Returns:
            dict: {
                'english': English text,
                'finnish': Finnish text,
                'raw': raw LLM response
            }
        """
        if history is None:
            history = []

        # Load onboarding system prompt
        system_prompt = self.prompts.load_onboarding()

        # Build conversation history
        conversation_context = "\n".join(
            f"User: {msg['user']}\nAISLE: {msg['ai']}" for msg in history
        )

        # Determine if this is the first message
        if not user_message:
            # No user input -> send introduction + first question
            full_prompt = (
                f"{system_prompt}\n\n"
                f"{conversation_context}\n\n"
                f"--- AISLE Introduction & First Question ---\n"
                f"User has not responded yet.\n"
                f"AISLE:"
            )
        else:
            # Normal onboarding step
            full_prompt = (
                f"{system_prompt}\n\n"
                f"{conversation_context}\n\n"
                f"--- New User Message ---\n"
                f"{user_message}\n\n"
                f"AISLE:"
            )

        # Call the LLM
        ai_response = self.llm.generate(full_prompt)

        # Parse response into English + Finnish
        english, finnish = "", ""
        for line in ai_response.splitlines():
            if line.lower().startswith("english:"):
                english = line.split(":", 1)[1].strip()
            elif line.lower().startswith("finnish:"):
                finnish = line.split(":", 1)[1].strip()

        return {
            "english": english,
            "finnish": finnish,
            "raw": ai_response
        }
