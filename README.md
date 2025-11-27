# AISLE

## Manual verification: initial assistant message

After opening the app and clicking to show the chat window, the frontend will automatically send an initial (empty) request to the backend and the assistant's first reply should appear without the user typing anything.

To test locally:

1. Start the backend server (from the `backend` folder).
2. Start the frontend dev server (from the `frontend` folder).
3. Open the web UI and open the chat window — you should see a "Thinking" bubble followed by the assistant's message.

If the assistant does not respond, check the frontend console and backend logs for fetch errors (API URL & CORS). The frontend currently posts to `http://127.0.0.1:5000/api/chat`, while the backend's route is `/chat` — if you run the backend directly you may need to ensure the endpoint matches or change the `API_URL` in `frontend/src/services/chatService.js`.

UI note: the assistant's response now shows both English and Finnish sections when available, using this format:

English:
<english response>

Suomi:
<Finnish response>

The frontend component `MessageBubble` will render both labeled sections if the backend returns `{ english, finnish }`.

Spacing notes:
 - To change how wide the chat area is, edit `frontend/src/styles.css` and adjust the `width` on `.chat-container` (currently `50vw` ~= 50% of the viewport). There is a responsive fallback for viewports <= 900px that makes the chat full-width.

Backend note — state updated correctly now:
- The backend previously could overwrite a session's state with an empty string returned by the model. I changed the code so empty model 'state' values are ignored (keeps the previous state) and session manager normalizes states to uppercase (e.g., `ONBOARDING`).
	To verify locally, watch the backend logs (start the server with `python backend/app.py`) and send a message from the frontend; you'll see lines like:

	Starting conversation for user <id>: state -> ONBOARDING
	Updating state for user <id>: ONBOARDING -> THEME_SELECTION

	If you're using Redis you can also inspect `session:default` to confirm the stored JSON contains the updated `state`.

Session handling note
- The app now uses a single server-side session (no per-user IDs). The backend stores state and history under a single session key (`session:default` in Redis). This simplifies local testing and avoids per-user session handling for now.
