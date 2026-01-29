"""
Borrow Service - Handle borrowing and returning logic
"""
from src.database.config import SessionLocal
from src.models import Transaction, Book, Fine
from src.models.transaction import TransactionType, TransactionStatus
from src.models.fine import FineStatus
from datetime import datetime, timedelta

class BorrowService:
    def __init__(self):
        self.session = SessionLocal()
        self.fine_per_day = 5  # Fine amount in currency units
        self.max_books_per_user = 5
        self.default_borrow_days = 14
    
    def borrow_book(self, user_id, book_id):
        """Borrow a book"""
        try:
            # Check if book exists and is available
            book = self.session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return False, "Book not found!"
            
            if book.available_copies <= 0:
                return False, "Book is not available!"
            
            # Check if user has reached max books limit
            active_borrows = self.session.query(Transaction).filter(
                (Transaction.user_id == user_id) &
                (Transaction.status == TransactionStatus.ACTIVE)
            ).count()
            
            if active_borrows >= self.max_books_per_user:
                return False, f"Maximum book limit ({self.max_books_per_user}) reached!"
            
            # Create transaction
            transaction = Transaction(
                user_id=user_id,
                book_id=book_id,
                transaction_type=TransactionType.BORROW,
                status=TransactionStatus.ACTIVE
            )
            transaction.set_due_date(self.default_borrow_days)
            
            # Update book availability
            book.available_copies -= 1
            
            self.session.add(transaction)
            self.session.commit()
            
            return True, f"Book '{book.title}' borrowed successfully! Due date: {transaction.due_date.date()}"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error borrowing book: {str(e)}"
    
    def return_book(self, transaction_id):
        """Return a borrowed book"""
        try:
            transaction = self.session.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()
            
            if not transaction:
                return False, "Transaction not found!"
            
            if transaction.status != TransactionStatus.ACTIVE:
                return False, "This transaction is already completed!"
            
            # Update transaction
            transaction.return_date = datetime.utcnow()
            transaction.status = TransactionStatus.COMPLETED
            
            # Update book availability
            book = self.session.query(Book).filter(Book.id == transaction.book_id).first()
            if book:
                book.available_copies += 1
            
            # Check for overdue and calculate fine
            if transaction.due_date and transaction.return_date > transaction.due_date:
                days_overdue = (transaction.return_date - transaction.due_date).days
                fine_amount = days_overdue * self.fine_per_day
                
                fine = Fine(
                    transaction_id=transaction.id,
                    user_id=transaction.user_id,
                    amount=fine_amount,
                    reason=f"Overdue by {days_overdue} days",
                    status=FineStatus.PENDING
                )
                self.session.add(fine)
                self.session.commit()
                return True, f"Book returned. Fine of {fine_amount} issued for {days_overdue} days overdue."
            
            self.session.commit()
            return True, "Book returned successfully!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error returning book: {str(e)}"
    
    def renew_book(self, transaction_id, additional_days=14):
        """Renew a borrowed book for additional days"""
        try:
            transaction = self.session.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()
            
            if not transaction:
                return False, "Transaction not found!"
            
            if transaction.status != TransactionStatus.ACTIVE:
                return False, "Can only renew active transactions!"
            
            # Extend due date
            old_due_date = transaction.due_date
            transaction.due_date = transaction.due_date + timedelta(days=additional_days)
            
            self.session.commit()
            return True, f"Book renewed! New due date: {transaction.due_date.date()}"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error renewing book: {str(e)}"
    
    def get_user_borrowed_books(self, user_id):
        """Get all books currently borrowed by a user"""
        return self.session.query(Transaction).filter(
            (Transaction.user_id == user_id) &
            (Transaction.status == TransactionStatus.ACTIVE)
        ).all()
    
    def get_overdue_transactions(self):
        """Get all overdue transactions"""
        current_time = datetime.utcnow()
        return self.session.query(Transaction).filter(
            (Transaction.due_date < current_time) &
            (Transaction.status == TransactionStatus.ACTIVE)
        ).all()
    
    def get_user_borrow_history(self, user_id):
        """Get borrow history for a user"""
        return self.session.query(Transaction).filter(
            Transaction.user_id == user_id
        ).all()
    
    def close(self):
        """Close database session"""
        self.session.close()
