from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from src.database.config import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    publication_year = Column(Integer, nullable=True)
    publisher = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
    
    def get_availability_status(self):
        """Get availability status"""
        return "Available" if self.available_copies > 0 else "Not Available"
