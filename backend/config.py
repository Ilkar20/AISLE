import os
from dotenv import load_dotenv

load_dotenv()

project_env = os.path.join(os.path.dirname(__file__), "env")
if os.path.exists(project_env):
    load_dotenv(dotenv_path=project_env, override=False)


class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

    @staticmethod
    def require_keys():
        """Raise a error if a required env var is missing.
        """
        if not Config.OPENROUTER_API_KEY:
            raise EnvironmentError(
                "OPENROUTER_API_KEY is missing. Set it in the environment or in a .env file."
            )
