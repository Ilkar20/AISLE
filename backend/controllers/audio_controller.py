# controllers/audio_controller.py
import os
import shutil
from fastapi import UploadFile
from services.transcription_service import transcribe_audio
from services.conversation_service import ConversationService

async def process_audio(file: UploadFile, session_id: str):
    temp_path = f"uploads/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Transcribe audio
    transcription = transcribe_audio(temp_path)

    # Pass transcription into ConversationService
    convo = ConversationService(session_id)
    ai_response = convo.handle_message(transcription)

    os.remove(temp_path)
    return {"userText": transcription, "aiResponse": ai_response}
s