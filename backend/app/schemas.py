# schemas.py - pydantic models (request/response shapes)

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRead(BaseModel):
    username: str
    id: int
class TokenPayload(BaseModel):
    sub: Optional[str] = None

class TransactionCreate(BaseModel):
    amount: int
    type: str
    category: str
    date: date

class TransactionRead(TransactionCreate):
    id: int
    user_id: int
