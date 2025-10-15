# routers/auth_router.py - endpoints for register/login

from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import UserCreate, Token, UserRead
from ..transactions import create_user, authenticate_user
from ..auth import create_access_token, get_current_user
from sqlmodel import Session
from ..database import get_session
from ..models import User
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate):
    try:
        user = create_user(user_in.username, user_in.password, user_in.full_name)
        token = create_access_token(subject=str(user.id))
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username already exists")

@router.post("/login", response_model=Token)
def login(form_data: UserCreate):
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token(subject=str(user.id))
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Login failed: {str(e)}")

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user