import requests
import json
from config import Config



class OpenRouterClient:
    BASE_URL = Config.OPENROUTER_URL

    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.model = model or Config.OPENROUTER_MODEL

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is missing in environment variables.")

    def generate(self, prompt_or_messages) -> str:
        """Send a message (string) or pre-built messages list to OpenRouter and
        return the raw text response.

        Accepts either:
          - prompt_or_messages: str -> will be wrapped into a basic messages list
          - prompt_or_messages: list[dict] -> used directly as "messages" payload
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Aisle Assistant",
        }

        # Build body depending on whether caller passed a plain prompt or
        # a prepared list of messages.
        if isinstance(prompt_or_messages, list):
            messages = prompt_or_messages
        else:
            # assume string
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": str(prompt_or_messages)}
            ]

        body = {"model": self.model, "messages": messages}

        response = requests.post(
            self.BASE_URL,
            headers = headers,
            data = json.dumps(body)
        )

        if response.status_code != 200:
            raise Exception(f"OpenRouter error: {response.text}")

        data = response.json()
        # Debug prints are useful while developing, but keep them minimal.
        print(data)

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise Exception(f"Unexpected OpenRouter response shape: {data}")

