"""
Database schema creation and initialization
"""
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create database if it doesn't exist"""
    USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() == 'true'
    
    if USE_SQLITE:
        # SQLite doesn't need database creation
        db_dir = "data"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        print(f"✓ SQLite database directory ready: {db_dir}/")
        return True
    
    # MySQL database creation
    try:
        import mysql.connector
        from mysql.connector import Error
        
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        cursor = connection.cursor()
        db_name = os.getenv('DB_NAME', 'library_management')
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created successfully or already exists.")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables using SQLAlchemy models"""
    try:
        from src.database.config import engine, Base
        from src.models import User, Book, Transaction, Fine
        
        if engine is None:
            print("Database engine not initialized!")
            return False
        
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def initialize_database():
    """Initialize complete database"""
    print("Initializing database...")
    
    if not create_database():
        return False
    
    if not create_tables():
        return False
    
    print("Database initialization completed!")
    return True

if __name__ == "__main__":
    initialize_database()
