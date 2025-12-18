# middleware/error_handler.py
from fastapi.responses import JSONResponse
from fastapi import Request

async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
