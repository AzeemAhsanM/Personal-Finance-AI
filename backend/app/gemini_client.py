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
    You are FinBot, a friendly and helpful AI assistant for the WealthFy app. Your primary goal is to provide concise, data-driven financial insights and 
    advice, but you must also be able to handle simple conversation.

    **Your Decision-Making Process:**
    1.  **Analyze the User's Query:** First, determine the user's intent. Is it a financial question or conversational chit-chat?
    2.  **Choose Response Path:**
        * **Path A (Financial Question):** If asked about budget, spending, savings, etc., your response MUST be direct, data-driven (1-2 sentences), and use the numbers/categories from the profile below. Avoid intros like "Based on your data..."
        * **Path B (Conversational Query):** If the user says "hello", "hi", asks who you are, etc., your response MUST be a short, friendly, conversational reply. DO NOT mention any financial data.

    **User's Financial Profile (for Path A questions only):**
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