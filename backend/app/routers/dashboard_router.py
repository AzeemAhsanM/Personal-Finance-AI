from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select
from sqlalchemy import func, case
from ..database import engine
from ..models import Transaction, User
from ..auth import decode_access_token, get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
def summary(current_user: User = Depends(get_current_user)):
    user_id = current_user.id # Get the user ID from the dependency
    with Session(engine) as session:
        # Totals
        income = session.exec(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(Transaction.user_id == user_id, Transaction.type == "income")
        ).one()
        expense = session.exec(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(Transaction.user_id == user_id, Transaction.type == "expense")
        ).one()

        # PostgreSQL-friendly date grouping
        monthly_summary = session.exec(
            select(
                func.to_char(Transaction.date, 'YYYY-MM').label("month"),
                func.sum(case((Transaction.type == "income", Transaction.amount), else_=0)).label("income"),
                func.sum(case((Transaction.type == "expense", Transaction.amount), else_=0)).label("expense"),
            )
            .where(Transaction.user_id == user_id)
            .group_by("month")
            .order_by("month")
        ).all()

        # Expense breakdown
        expense_breakdown = session.exec(
            select(
                Transaction.category.label("name"),
                func.sum(Transaction.amount).label("amount")
            )
            .where(Transaction.user_id == user_id, Transaction.type == "expense")
            .group_by(Transaction.category)
        ).all()

        # Recent transactions
        recent_transactions = session.exec(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.date.desc())
            .limit(5)
        ).all()

    return {
        "total_balance": float(income) - float(expense),
        "monthly_summary": [dict(row._mapping) for row in monthly_summary],
        "expense_breakdown": [dict(row._mapping) for row in expense_breakdown],
        "recent_transactions": recent_transactions,
    }