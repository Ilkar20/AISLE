# backend/llm_mock.py
"""
A tiny deterministic 'LLM' that simply returns bilingual text structures.
Replace with real LLM client (ollama_client) later.
"""

class LLMMock:
    def generate(self, prompt):
        # prompt is a dict {"fi": "...", "en": "..."} or a string
        # If it is already structured, echo back; otherwise return generic message
        if isinstance(prompt, dict):
            return {"fi": prompt.get("fi"), "en": prompt.get("en")}
        # fallback
        return {"fi": str(prompt), "en": str(prompt)}
