"""
Report Service - Generate reports and export to CSV/PDF
"""
from src.database.config import SessionLocal
from src.models import Book, Transaction, Fine, User
from src.models.transaction import TransactionStatus
from src.models.fine import FineStatus
from datetime import datetime
from sqlalchemy import func, desc
import csv
import os

class ReportService:
    def __init__(self):
        self.session = SessionLocal()
        self.reports_dir = "data/reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def get_popular_books(self, limit=10):
        """Get most borrowed/popular books"""
        popular_books = self.session.query(
            Book.id,
            Book.title,
            Book.author,
            func.count(Transaction.id).label('borrow_count')
        ).join(Transaction, Book.id == Transaction.book_id).group_by(
            Book.id
        ).order_by(desc('borrow_count')).limit(limit).all()
        
        return popular_books
    
    def get_overdue_books(self):
        """Get list of overdue books and users"""
        from datetime import datetime
        current_time = datetime.utcnow()
        
        overdue = self.session.query(
            Transaction.id,
            User.full_name,
            User.email,
            Book.title,
            Transaction.due_date,
            func.datediff(current_time, Transaction.due_date).label('days_overdue')
        ).join(User, Transaction.user_id == User.id).join(
            Book, Transaction.book_id == Book.id
        ).filter(
            (Transaction.due_date < current_time) &
            (Transaction.status == TransactionStatus.ACTIVE)
        ).all()
        
        return overdue
    
    def get_inventory_status(self):
        """Get library inventory status"""
        inventory = self.session.query(
            Book.title,
            Book.author,
            Book.total_copies,
            Book.available_copies,
            (Book.total_copies - Book.available_copies).label('borrowed_copies')
        ).all()
        
        return inventory
    
    def get_user_activity(self, user_id):
        """Get activity history for a specific user"""
        transactions = self.session.query(Transaction).filter(
            Transaction.user_id == user_id
        ).all()
        
        return transactions
    
    def get_fine_statistics(self):
        """Get fine statistics"""
        fine_stats = self.session.query(
            User.full_name,
            User.email,
            func.count(Fine.id).label('total_fines'),
            func.sum(Fine.amount).label('total_amount'),
            func.count(Fine.id).filter(Fine.status == FineStatus.PENDING).label('pending_fines')
        ).join(Fine, User.id == Fine.user_id).group_by(
            User.id
        ).all()
        
        return fine_stats
    
    def export_popular_books_csv(self, filename=None):
        """Export popular books to CSV"""
        if not filename:
            filename = f"popular_books_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.reports_dir, filename)
        popular_books = self.get_popular_books()
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Book ID', 'Title', 'Author', 'Times Borrowed'])
                for book in popular_books:
                    writer.writerow(book)
            
            return True, f"Report exported to {filepath}"
        except Exception as e:
            return False, f"Error exporting report: {str(e)}"
    
    def export_overdue_books_csv(self, filename=None):
        """Export overdue books to CSV"""
        if not filename:
            filename = f"overdue_books_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.reports_dir, filename)
        overdue = self.get_overdue_books()
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Transaction ID', 'User Name', 'Email', 'Book Title', 'Due Date', 'Days Overdue'])
                for item in overdue:
                    writer.writerow(item)
            
            return True, f"Report exported to {filepath}"
        except Exception as e:
            return False, f"Error exporting report: {str(e)}"
    
    def export_inventory_csv(self, filename=None):
        """Export inventory status to CSV"""
        if not filename:
            filename = f"inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.reports_dir, filename)
        inventory = self.get_inventory_status()
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Title', 'Author', 'Total Copies', 'Available Copies', 'Borrowed Copies'])
                for item in inventory:
                    writer.writerow(item)
            
            return True, f"Report exported to {filepath}"
        except Exception as e:
            return False, f"Error exporting report: {str(e)}"
    
    def export_fine_statistics_csv(self, filename=None):
        """Export fine statistics to CSV"""
        if not filename:
            filename = f"fine_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.reports_dir, filename)
        stats = self.get_fine_statistics()
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User Name', 'Email', 'Total Fines', 'Total Amount', 'Pending Fines'])
                for item in stats:
                    writer.writerow(item)
            
            return True, f"Report exported to {filepath}"
        except Exception as e:
            return False, f"Error exporting report: {str(e)}"
    
    def close(self):
        """Close database session"""
        self.session.close()
