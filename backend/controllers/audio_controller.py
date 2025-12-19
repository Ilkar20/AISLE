# controllers/audio_controller.py
import os
from services.transcription_service import transcribe_audio
from services.conversation_service import ConversationService

UPLOAD_DIR = "uploads"

def process_audio(file, session_id: str):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(temp_path)

    # Step 1: Transcribe audio
    transcription = transcribe_audio(temp_path)

    # Step 2: Pass transcription into ConversationService
    convo = ConversationService(session_id)
    ai_response = convo.handle_message(transcription)

    os.remove(temp_path)
    return {"userText": transcription, "aiResponse": ai_response}
