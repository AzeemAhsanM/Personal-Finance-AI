# routers/transactions_router.py

from fastapi import APIRouter, Depends
from typing import List
from ..schemas import TransactionCreate, TransactionRead
from ..models import User
from ..transactions import create_transaction, list_transactions
from ..auth import get_current_user 

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionRead)
def add_transaction(tx: TransactionCreate, current_user: User = Depends(get_current_user)):
    return create_transaction(current_user.id, tx)

@router.get("/list", response_model=List[TransactionRead])
def get_transactions(current_user: User = Depends(get_current_user)):
    return list_transactions(current_user.id)