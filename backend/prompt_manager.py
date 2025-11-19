import os

class PromptManager:
    def __init__(self, template_dir="prompts"):
        self.template_dir = template_dir

    def load_onboarding(self):
        path = os.path.join(self.template_dir, "on boarding.txt")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()