# database.py - database connection and engine setup

from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # load .env in development

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:azeem@localhost:5432/finance_db")

# For SQLModel + asyncpg you'd typically use databases/async engines.
# We'll define a synchronous engine for simple usage here.
engine = create_engine(DATABASE_URL, echo=True)

# Create sessionmaker for SQLAlchemy sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    # Create DB tables from models (SQLModel metadata)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
