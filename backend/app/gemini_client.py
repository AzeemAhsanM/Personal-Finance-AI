import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()   

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY ")

# Configure Gemini SDK
genai.configure(api_key=GEMINI_API_KEY)


async def get_financial_advice(message: str, user_data: dict, user_id: int):
    """
    Acts as a financial data assistant, providing short, data-driven answers.
    """
    # --- Format the expense breakdown for the prompt ---
    expense_breakdown_dict = user_data.get('expense_breakdown', {})
    if expense_breakdown_dict:
        breakdown_str = "\n".join(
            [f"    - {category}: ${amount:.2f}" for category, amount in expense_breakdown_dict.items()]
        )
    else:
        breakdown_str = "    No categorized expenses found."
    # ---------------------------------------------------

    # --- Prompt Engineering: Define the AI's Persona and Context ---
    prompt = f"""
System: You are FinBot. Provide ultra-concise, data-driven financial advice for the WealthFy app.

Rules:
1. Intent: If greeting (hi/hello), reply with a 1-sentence friendly greeting. No data.
2. Financials: For all other queries, answer in 1-2 sentences using the data below.
3. Scope: Cover spending, savings, investment plans, and tax optimization.
4. Tone: No intros ("Based on your data..."). Start immediately with the insight.

User Data:
    - Income: ₹{user_data.get('income', 'N/A')}
    - Expenses: ₹{user_data.get('expenses', 'N/A')}
    - Net Balance: ₹{user_data.get('net', 'N/A')}
    - Expense Breakdown:
{breakdown_str}

    **User's Question:** "{message}"
    """
    # --------------------------------------------------------------------
    try:
        # Use a fast model for quick chat-like responses
        model = genai.GenerativeModel("models/gemini-flash-latest")
        response = model.generate_content(prompt)
        return {"reply": response.text}

    except Exception as e:
        return {"error": f"Gemini API request failed: {str(e)}"}