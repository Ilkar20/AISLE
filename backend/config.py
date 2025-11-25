import os
from dotenv import load_dotenv

# Try to load common env files: first " .env " then fallback to "env" if present.
# Many repos use a file named `env` by mistake — we'll load both so the app works
# either way.
load_dotenv()  # default looks for a .env file in cwd

# Fallback: attempt to load a plain `env` file in the project directory
project_env = os.path.join(os.path.dirname(__file__), "env")
if os.path.exists(project_env):
    load_dotenv(dotenv_path=project_env, override=False)


class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

    @staticmethod
    def require_keys():
        """Raise a helpful error if a required env var is missing.

        This isn't invoked automatically anywhere in the codebase; callers
        can use it to get a clear, actionable message about missing variables.
        """
        if not Config.OPENROUTER_API_KEY:
            raise EnvironmentError(
                "OPENROUTER_API_KEY is missing. Set it in the environment or in a .env (or env) file."
            )
