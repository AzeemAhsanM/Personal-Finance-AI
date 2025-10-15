# crud.py - functions to read/write DB

from sqlmodel import select
from .models import User, Transaction
from .auth import get_password_hash, verify_password
from .database import engine
from sqlmodel import Session
from typing import Optional
from datetime import date
from sqlalchemy import func

def create_user(username: str, password: str, full_name: Optional[str] = None):
    user = User(username=username, hashed_password=get_password_hash(password), full_name=full_name)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

def authenticate_user(username: str, password: str) -> Optional[User]:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

def create_transaction(user_id: int, tx_data):
    tx = Transaction(user_id=user_id, **tx_data.dict())
    with Session(engine) as session:
        session.add(tx)
        session.commit()
        session.refresh(tx)
    return tx

def list_transactions(user_id: int):
    with Session(engine) as session:
        rows = session.exec(select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.date.desc())).all()
    return rows

# def aggregate_summary(user_id: int):
#     # total income - expense
#     with Session(engine) as session:
#         income = session.exec(select(func.coalesce(func.sum(Transaction.amount), 0)).where(Transaction.user_id == user_id, Transaction.type == "income")).one()
#         expense = session.exec(select(func.coalesce(func.sum(Transaction.amount), 0)).where(Transaction.user_id == user_id, Transaction.type == "expense")).one()
#     return {"income": float(income), "expense": float(expense), "net": float(income) - float(expense)}
