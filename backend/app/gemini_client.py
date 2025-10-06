# gemini_client.py - adapter to send messages to Gemini-like API

import os
import httpx

GEMINI_API_URL = os.getenv("GEMINI_API_URL")  # e.g., https://api.gemini.example/v1/generate
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def ask_gemini(message: str, user_id: int):
    if not GEMINI_API_URL or not GEMINI_API_KEY:
        return {"error": "Gemini API not configured."}
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "input": message,
        "user": str(user_id)
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(GEMINI_API_URL, json=payload, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return resp.json()
