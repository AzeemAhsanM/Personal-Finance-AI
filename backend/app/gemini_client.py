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
    You are FinBot, an AI assistant integrated into a personal finance dashboard.
    Your goal is to answer the user's question directly and concisely using their financial data.

    **CRITICAL RULES:**
    1.  **Be extremely brief.** Your answer must be one or two sentences maximum.
    2.  **Be direct.** Get straight to the point without any introductory phrases like "Based on your data..."
    3.  **Use the data.** Your answer MUST be based only on the financial profile provided below. Use the numbers and categories directly in your response. Do not give generic advice.

    **User's Financial Profile:**
    - Income: ${user_data.get('income', 'N/A')}
    - Expenses: ${user_data.get('expenses', 'N/A')}
    - Net Balance: ${user_data.get('net', 'N/A')}
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