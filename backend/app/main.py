# main.py - FastAPI application entrypoint

from fastapi import FastAPI
from contextlib import asynccontextmanager  
from .database import create_db_and_tables
from .routers import auth_router, transactions_router, dashboard_router, ai_router
from fastapi.middleware.cors import CORSMiddleware
from .logger import logger
import os

# 2. Define the new lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    logger.info("Starting up and creating database tables...")
    create_db_and_tables()
    yield
    # Code to run on shutdown (if any)
    logger.info("Shutting down...")

# 3. Pass the lifespan function to the FastAPI app
app = FastAPI(title="WealthFy", lifespan=lifespan)

# This list allows requests from both your live website and your local computer.
origins = [
    "https://wealthfy.site",  # Your production frontend
    "http://localhost:3000",   # Your local development frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)
app.include_router(transactions_router.router)
app.include_router(dashboard_router.router)
app.include_router(ai_router.router)
