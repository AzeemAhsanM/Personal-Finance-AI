from fastapi import APIRouter, Depends, HTTPException, Header
from collections import defaultdict
from sqlmodel import Session, select
from ..gemini_client import get_financial_advice
from ..auth import decode_access_token
from ..database import get_session
from ..models import Transaction

router = APIRouter(prefix="/ai", tags=["ai"])

def get_current_user_id(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

# --- Real Database Function (Corrected) ---
# This function now correctly gets the user_id from the authentication dependency.
async def get_user_financial_data(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_session)) -> dict:
    """
    Fetches and aggregates a user's financial data from the database,
    including a breakdown of expenses by category.
    """
    statement = select(Transaction).where(Transaction.user_id == user_id)
    transactions = db.exec(statement).all()

    total_income = sum(tx.amount for tx in transactions if tx.type == 'income')
    total_expenses = sum(tx.amount for tx in transactions if tx.type == 'expense')
    net_balance = total_income - total_expenses

    # Calculate expense breakdown by category
    expense_breakdown = defaultdict(float)
    for tx in transactions:
        if tx.type == 'expense':
            expense_breakdown[tx.category] += tx.amount

    return {
        "income": total_income,
        "expenses": total_expenses,
        "net": net_balance,
        "expense_breakdown": dict(expense_breakdown)
    }
# -------------------------------------

@router.post("/chat")
async def chat(message: dict, user_data: dict = Depends(get_user_financial_data), user_id: int = Depends(get_current_user_id)):
    text = message.get("message")
    if not text:
        raise HTTPException(status_code=400, detail="No message")

    response = await get_financial_advice(text, user_data, user_id)

    return response