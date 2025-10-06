# models.py - database models using SQLModel

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    transactions: List["Transaction"] = Relationship(back_populates="user")

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    amount: float
    type: str  # "income" or "expense"
    category: Optional[str] = None
    description: Optional[str] = None
    date: date

    user: Optional[User] = Relationship(back_populates="transactions")
