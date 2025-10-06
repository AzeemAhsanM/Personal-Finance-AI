# routers/dashboard_router.py - endpoints for aggregated data

from fastapi import APIRouter, Depends
from ..transactions import aggregate_summary
from ..auth import decode_access_token
from fastapi import Header, HTTPException

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def get_current_user_id(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.get("/summary")
def summary(user_id: int = Depends(get_current_user_id)):
    return aggregate_summary(user_id)
