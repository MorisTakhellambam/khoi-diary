# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = "postgresql://neondb_owner:npg_RJukx4IeG0pw@ep-proud-pine-a1hbfor8-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Ensure it’s Postgres, not SQLite
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Optional: force SSL mode (Neon requires it)
if "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
