import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use SQLite by default (no MySQL needed!)
USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() == 'true'

if USE_SQLITE:
    # SQLite database (works without MySQL)
    DB_FILE = "data/library.db"
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    DATABASE_URL = f"sqlite:///{DB_FILE}"
    print("✓ Using SQLite database (no MySQL needed)")
else:
    # MySQL database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'library_management')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print("✓ Using MySQL database")

try:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
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
