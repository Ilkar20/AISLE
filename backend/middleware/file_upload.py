# middleware/file_upload.py
from fastapi import HTTPException

ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a"}

def validate_file(filename: str):
    ext = filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")
