from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, String
from datetime import datetime
import enum
from src.database.config import Base

class FineStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    WAIVED = "waived"

class Fine(Base):
    __tablename__ = "fines"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    reason = Column(String(255), nullable=False)  # e.g., "Overdue by X days"
    status = Column(Enum(FineStatus), default=FineStatus.PENDING)
    issued_date = Column(DateTime, default=datetime.utcnow)
    paid_date = Column(DateTime, nullable=True)
    notes = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Fine User:{self.user_id} Amount:{self.amount}>"
