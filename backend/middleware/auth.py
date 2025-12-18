# middleware/auth.py
from fastapi import Request, HTTPException

async def check_api_key(request: Request, call_next):
    api_key = request.headers.get("x-api-key")
    if api_key != "expected-secret":
        raise HTTPException(status_code=403, detail="Forbidden")
    return await call_next(request)
