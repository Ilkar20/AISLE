import os

class PromptManager:
    def __init__(self, templates_dir="prompts"):
        self.templates_dir = templates_dir
        self.state_to_prompt = {
            "ONBOARDING": "onboarding.txt",
            "THEME_SELECTION": "theme.txt",
            "SITUATION_SELECTION": "situation.txt",
            "EXERCISE": "exercise.txt",
            "FEEDBACK": "feedback.txt",
            "DASHBOARD": "dashboard.txt"
        }
        self.system_base = self.load_template("onboarding.txt")

    def load_template(self, filename):
        path = os.path.join(self.templates_dir, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Fail gracefully and show which file is missing — caller
            # may fall back to empty responses.
            raise FileNotFoundError(f"Missing prompt template: {path}")

    def get_state_prompt(self, state):
        """
        Returns the template content for the given state.
        Falls back to empty string if no template exists.
        """
        state_upper = state.upper()
        filename = self.state_to_prompt.get(state_upper)
        if not filename:
            return ""
        return self.load_template(filename)