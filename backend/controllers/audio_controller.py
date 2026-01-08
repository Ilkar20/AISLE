# controllers/audio_controller.py
from services.transcription_service import transcribe_audio
from services.conversation_service import ConversationService

def process_audio(file_path: str, session_id: str):
    """
    Process an uploaded audio file: transcribe and update conversation.
    Expects a file path string (saved by audio_routes).
    """
    # Step 1: Transcribe audio
    transcription = transcribe_audio(file_path)

    # Step 2: Pass transcription into ConversationService
    convo = ConversationService(session_id)
    ai_response = convo.handle_message(transcription)

    return {
        "userText": transcription,
        "aiResponse": ai_response,
        "session_id": session_id
    }
