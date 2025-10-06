# auth.py - authentication utilities (hashing and JWT)

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def get_password_hash(password: str) -> str:
    return PWD_CTX.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CTX.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: timedelta = None):
    now = datetime.utcnow()
    exp = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": subject, "iat": now, "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
