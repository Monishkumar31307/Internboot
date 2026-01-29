from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
from src.database.config import Base

class TransactionType(enum.Enum):
    BORROW = "borrow"
    RETURN = "return"

class TransactionStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.ACTIVE)
    notes = Column(String(255), nullable=True)
    
    # Relationships
    user = relationship("User")
    book = relationship("Book")
    
    def set_due_date(self, days=14):
        """Set due date (default 14 days from borrow date)"""
        self.due_date = self.borrow_date + timedelta(days=days)
    
    def is_overdue(self):
        """Check if transaction is overdue"""
        if self.due_date and not self.return_date:
            return datetime.utcnow() > self.due_date
        return False
    
    def get_days_overdue(self):
        """Get number of days overdue"""
        if self.is_overdue():
            return (datetime.utcnow() - self.due_date).days
        return 0
    
    def __repr__(self):
        return f"<Transaction User:{self.user_id} Book:{self.book_id}>"
