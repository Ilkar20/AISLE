import requests
import json
from config import Config

class OpenRouterClient:
    BASE_URL = Config.OPENROUTER_URL

    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.model = Config.OPENROUTER_MODEL
        
        with open("prompts/aisle_master.txt", "r", encoding="utf-8") as f:
            self.master_prompt = f.read()

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is missing in environment variables.")

    def generate(self, prompt_or_messages) -> str:
        """
        Accepts either:
          - str: will be wrapped into a basic messages list
          - list[dict]: used directly as "messages" payload
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Aisle Assistant",
        }

        # Normalize messages
        if isinstance(prompt_or_messages, str):
            messages = [
                {"role": "system", "content": self.master_prompt},
                {"role": "user", "content": prompt_or_messages},
            ]
        elif isinstance(prompt_or_messages, list):
            normalized = []
            for msg in prompt_or_messages:
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    normalized.append(msg)
                else:
                    # fallback: wrap raw strings or malformed entries
                    normalized.append({"role": "user", "content": str(msg)})
            messages = [{"role": "system", "content": self.master_prompt}] + normalized
        else:
            raise TypeError("prompt_or_messages must be str or list[dict]")

        body = {"model": self.model, "messages": messages}

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=body
        )

        if response.status_code != 200:
            raise Exception(f"OpenRouter error: {response.text}")

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise Exception(f"Unexpected OpenRouter response shape: {data}")
