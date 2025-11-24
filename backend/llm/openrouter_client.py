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

    def generate(self, prompt: str) -> str:
        """Send a message to OpenRouter and return the raw text response."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Aisle Assistant",
        }

        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            self.BASE_URL,
            headers = headers,
            data = json.dumps(body)
        )

        if response.status_code != 200:
            raise Exception(f"OpenRouter error: {response.text}")

        data = response.json()
        print (data)
        return data["choices"][0]["message"]["content"]

