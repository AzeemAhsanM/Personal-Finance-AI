# routers/auth_router.py - endpoints for register/login

from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import UserCreate, Token
from ..transactions import create_user, authenticate_user
from ..auth import create_access_token
from sqlmodel import Session
from ..database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate):
    user = create_user(user_in.email, user_in.password, user_in.full_name)
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: UserCreate):
    user = authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
