# routes/audio_routes.py
from fastapi import APIRouter, UploadFile, Form
from controllers.audio_controller import process_audio

router = APIRouter()

@router.post("/upload")
async def upload_audio(file: UploadFile, session_id: str = Form(...)):
    return await process_audio(file, session_id)
