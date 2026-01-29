"""
Database configuration using SQLite (No MySQL needed!)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file location
DB_FILE = "data/library.db"

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# Create database URL for SQLite
DATABASE_URL = f"sqlite:///{DB_FILE}"

try:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print(f"✓ Database configured: {DB_FILE}")
except Exception as e:
    print(f"Error connecting to database: {e}")
    engine = None
    SessionLocal = None
    Base = declarative_base()

def get_db():
    """Get database session"""
    if SessionLocal:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        raise Exception("Database connection not initialized")
