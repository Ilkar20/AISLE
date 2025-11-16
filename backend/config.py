# backend/config.py
import os

# Basic env-driven config. Use environment variables in production.
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
HOST = os.getenv("APP_HOST", "127.0.0.1")
PORT = int(os.getenv("APP_PORT", 5000))
DEBUG = os.getenv("DEBUG", "true").lower() in ("1", "true", "yes")

PROMPT_TEMPLATES_PATH = os.getenv("PROMPT_TEMPLATES_PATH", "prompt_templates")
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", 60 * 60 * 24))  # 24h
