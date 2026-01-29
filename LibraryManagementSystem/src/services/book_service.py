"""
Book Service - Search, Filter, and Management
"""
from src.database.config import SessionLocal
from src.models import Book
from sqlalchemy import or_, and_
from datetime import datetime

class BookService:
    def __init__(self):
        self.session = SessionLocal()
    
    def add_book(self, title, author, genre, isbn, publication_year=None, 
                 publisher=None, description=None, total_copies=1, price=None):
        """Add a new book to the library"""
        try:
            # Check if ISBN already exists
            existing_book = self.session.query(Book).filter(Book.isbn == isbn).first()
            if existing_book:
                return False, "Book with this ISBN already exists!"
            
            new_book = Book(
                title=title,
                author=author,
                genre=genre,
                isbn=isbn,
                publication_year=publication_year,
                publisher=publisher,
                description=description,
                total_copies=total_copies,
                available_copies=total_copies,
                price=price
            )
            
            self.session.add(new_book)
            self.session.commit()
            return True, f"Book '{title}' added successfully!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error adding book: {str(e)}"
    
    def search_by_title(self, title):
        """Search books by title"""
        return self.session.query(Book).filter(
            Book.title.ilike(f"%{title}%")
        ).all()
    
    def search_by_author(self, author):
        """Search books by author"""
        return self.session.query(Book).filter(
            Book.author.ilike(f"%{author}%")
        ).all()
    
    def search_by_genre(self, genre):
        """Search books by genre"""
        return self.session.query(Book).filter(
            Book.genre.ilike(f"%{genre}%")
        ).all()
    
    def search_by_isbn(self, isbn):
        """Search book by ISBN"""
        return self.session.query(Book).filter(Book.isbn == isbn).first()
    
    def filter_available_books(self):
        """Get all available books"""
        return self.session.query(Book).filter(Book.available_copies > 0).all()
    
    def filter_unavailable_books(self):
        """Get all unavailable books"""
        return self.session.query(Book).filter(Book.available_copies == 0).all()
    
    def advanced_search(self, title=None, author=None, genre=None, availability=None):
        """Advanced search with multiple filters"""
        query = self.session.query(Book)
        
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if genre:
            query = query.filter(Book.genre.ilike(f"%{genre}%"))
        if availability is not None:
            if availability:  # True = available
                query = query.filter(Book.available_copies > 0)
            else:  # False = unavailable
                query = query.filter(Book.available_copies == 0)
        
        return query.all()
    
    def get_book_by_id(self, book_id):
        """Get book by ID"""
        return self.session.query(Book).filter(Book.id == book_id).first()
    
    def get_all_books(self):
        """Get all books"""
        return self.session.query(Book).all()
    
    def update_book(self, book_id, **kwargs):
        """Update book details"""
        try:
            book = self.session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return False, "Book not found!"
            
            for key, value in kwargs.items():
                if hasattr(book, key) and key not in ['id', 'created_at']:
                    setattr(book, key, value)
            
            book.updated_at = datetime.utcnow()
            self.session.commit()
            return True, "Book updated successfully!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error updating book: {str(e)}"
    
    def delete_book(self, book_id):
        """Delete a book"""
        try:
            book = self.session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return False, "Book not found!"
            
            self.session.delete(book)
            self.session.commit()
            return True, "Book deleted successfully!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error deleting book: {str(e)}"
    
    def close(self):
        """Close database session"""
        self.session.close()
