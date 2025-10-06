# routers/ai_router.py - FinBot proxy endpoint

from fastapi import APIRouter, Depends, HTTPException, Header
from ..gemini_client import ask_gemini
from ..auth import decode_access_token

router = APIRouter(prefix="/ai", tags=["ai"])

def get_current_user_id(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/chat")
async def chat(message: dict, user_id: int = Depends(get_current_user_id)):
    # message should be {"message": "Hello"}
    text = message.get("message")
    if not text:
        raise HTTPException(status_code=400, detail="No message")
    response = await ask_gemini(text, user_id)
    return response
