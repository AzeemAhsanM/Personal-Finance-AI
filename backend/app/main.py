# main.py - FastAPI application entrypoint

from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import auth_router, transactions_router, dashboard_router, ai_router
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI(title="WealthFy")

# allow CORS from frontend dev server
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router.router)
app.include_router(transactions_router.router)
app.include_router(dashboard_router.router)
app.include_router(ai_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)