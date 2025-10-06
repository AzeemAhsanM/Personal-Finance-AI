# routers/transactions_router.py - protected CRUD endpoints for transactions

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas import TransactionCreate, TransactionRead
from ..transactions import create_transaction, list_transactions
from ..auth import decode_access_token
from fastapi import Header

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_current_user_id(authorization: str = Header(...)):
    # expects "Bearer <token>"
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/", response_model=TransactionRead)
def add_transaction(tx: TransactionCreate, user_id: int = Depends(get_current_user_id)):
    return create_transaction(user_id, tx)

@router.get("/", response_model=List[TransactionRead])
def get_transactions(user_id: int = Depends(get_current_user_id)):
    return list_transactions(user_id)
