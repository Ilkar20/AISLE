import os

class PromptManager:
    def __init__(self, templates_dir="prompt_templates"):
        self.templates_dir = templates_dir
        self.state_to_prompt = {
            "ONBOARDING": "onboarding_prompt.txt",
            "THEME_SELECTION": "theme_prompt.txt",
            "SITUATION_SELECTION": "situation_prompt.txt",
            "EXERCISE": "exercise_prompt.txt",
            "FEEDBACK": "feedback_prompt.txt",
            "DASHBOARD": "dashboard_prompt.txt"
        }
        self.system_base = self.load_template("system_base.txt")

    def load_template(self, filename):
        path = os.path.join(self.templates_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def get_state_prompt(self, state):
        """
        Returns the template content for the given state.
        Falls back to empty string if no template exists.
        """
        filename = self.state_to_prompt.get(state)
        if not filename:
            return ""
        return self.load_template(filename)

    def get_system_prompt(self):
        return self.system_base
