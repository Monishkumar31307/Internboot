"""
Fine Service - Handle fines management
"""
from src.database.config import SessionLocal
from src.models import Fine, User
from src.models.fine import FineStatus
from datetime import datetime

class FineService:
    def __init__(self):
        self.session = SessionLocal()
    
    def get_user_fines(self, user_id):
        """Get all fines for a user"""
        return self.session.query(Fine).filter(Fine.user_id == user_id).all()
    
    def get_pending_fines(self, user_id):
        """Get pending fines for a user"""
        return self.session.query(Fine).filter(
            (Fine.user_id == user_id) &
            (Fine.status == FineStatus.PENDING)
        ).all()
    
    def get_total_pending_fine_amount(self, user_id):
        """Get total pending fine amount for a user"""
        from sqlalchemy import func
        total = self.session.query(func.sum(Fine.amount)).filter(
            (Fine.user_id == user_id) &
            (Fine.status == FineStatus.PENDING)
        ).scalar()
        
        return total if total else 0
    
    def pay_fine(self, fine_id):
        """Mark a fine as paid"""
        try:
            fine = self.session.query(Fine).filter(Fine.id == fine_id).first()
            
            if not fine:
                return False, "Fine not found!"
            
            if fine.status != FineStatus.PENDING:
                return False, f"Fine is already {fine.status.value}!"
            
            fine.status = FineStatus.PAID
            fine.paid_date = datetime.utcnow()
            
            self.session.commit()
            return True, f"Fine of {fine.amount} paid successfully!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error paying fine: {str(e)}"
    
    def waive_fine(self, fine_id, reason=None):
        """Waive a fine (admin only)"""
        try:
            fine = self.session.query(Fine).filter(Fine.id == fine_id).first()
            
            if not fine:
                return False, "Fine not found!"
            
            fine.status = FineStatus.WAIVED
            if reason:
                fine.notes = reason
            
            self.session.commit()
            return True, f"Fine of {fine.amount} waived!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error waiving fine: {str(e)}"
    
    def close(self):
        """Close database session"""
        self.session.close()
