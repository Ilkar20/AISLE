## AISLE — Copilot instructions

Purpose: give an AI coding agent immediate, actionable context to work on this repository.

- **Big picture**: single-page frontend (`frontend/src`) talks to a small Flask backend (`backend/`) over HTTP. The backend is single-session by design (stores one session in Redis under `session:default`) and orchestrates prompts -> LLM -> parser -> session store.

- **Request flow**: `frontend` -> POST `/chat` (see `backend/router.py`) -> `ConversationService.handle_message` (`backend/conversation_service.py`) -> `OpenRouterClient.generate` (`backend/llm/openrouter_client.py`) -> parse via `backend/utils/parser.py` -> update `RedisSessionManager` (`backend/session_manager.py`) -> return JSON to frontend.

- **Key files to inspect for changes or examples**:
  - `backend/app.py` — Flask app + CORS and blueprint registration
  - `backend/router.py` — request entrypoint for `/chat`
  - `backend/conversation_service.py` — core orchestration and business logic
  - `backend/session_manager.py` — single-session Redis state & history (note: methods do NOT accept a session_id)
  - `backend/llm/openrouter_client.py` — LLM integration; requires `Config.OPENROUTER_API_KEY` and `OPENROUTER_URL`/`MODEL`
  - `backend/prompt_manager.py` and `backend/prompts/*.txt` — state-to-prompt templates
  - `backend/utils/parser.py` — tolerant JSON extraction from LLM text output
  - `frontend/src/services/chatService.js` — frontend API URL used by the UI

- **Project-specific conventions** (do not assume standard defaults):
  - Single-session mode: session data is stored under Redis key `session:default`. Methods in `RedisSessionManager` are written for one session and therefore take no `session_id` argument.
  - States are canonicalized to UPPERCASE by the session manager (`set_state` calls `.upper()`). Use uppercase state strings when writing tests or prompt templates.
  - Parser is permissive: `parse_ai_response` extracts the first JSON object from LLM output. Prefer returning clean JSON from the model, but code tolerates extra text/formatting.
  - UTF-8 handling: `decode_responses=True` in Redis client and `ensure_ascii=False` when writing JSON to preserve Finnish characters (ä, ö, å).

- **Common pitfalls / debugging tips**:
  - TypeError like `get_session() takes 1 positional argument but 2 were given`: this happens because `conversation_service.py` currently calls session methods with a `session_id` argument (e.g. `self.sessions.get_session(session_id)`) while `RedisSessionManager` defines `get_session(self)` (no param). Fix by either:
    - Preferred quick fix: remove the extra `session_id` argument calls in `conversation_service.py` and call `self.sessions.get_session()`, `self.sessions.get_state()`, etc., because the project is single-session.
    - Or, if you want to support multiple sessions: update `RedisSessionManager` signatures to accept a `session_id` and use it to build Redis keys (e.g. `session:{session_id}`).
  - Missing env vars: `OPENROUTER_API_KEY` and Redis vars are loaded from environment; ensure `.env` or host env is configured. `OpenRouterClient.__init__` raises if API key missing.
  - Endpoint mismatch: README warns the frontend may point to `http://127.0.0.1:5000/api/chat` while router exposes `/chat`. Check `frontend/src/services/chatService.js` and align `API_URL`.

- **How to run & quick tests (PowerShell)**:
  - Start backend (from repo root or `backend`):

```powershell
cd backend
python .\app.py
```

  - Quick POST test (PowerShell):

```powershell
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:5000/chat' -ContentType 'application/json' -Body '{"message":"Hello"}'
```

- **When editing code**:
  - Preserve single-session assumption unless you intentionally add multi-session support — changing session storage shape affects multiple modules (`conversation_service.py`, `session_manager.py`, and tests).
  - When modifying LLM prompts, edit files in `backend/prompts/` and prefer `PromptManager.get_state_prompt(state)` for state-specific templates.
  - Keep `english` / `finnish` fields in responses (frontend `MessageBubble` expects both). `parse_ai_response` returns `{ english, finnish, state }`.

- **If you update this file**: keep it short and factual. This file is the canonical, runnable summary an AI agent should read before editing code.

If anything here looks incomplete or you want me to expand a specific area (e.g. make a small patch to fix the `session_id` mismatch), tell me which part to prioritize.
