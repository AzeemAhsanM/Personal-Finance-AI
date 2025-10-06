# schemas.py - pydantic models (request/response shapes)

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: Optional[str] = None
    description: Optional[str] = None
    date: date

class TransactionRead(TransactionCreate):
    id: int
    user_id: int
