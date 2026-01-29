"""
Sample data loader for the library management system
"""
from src.services.auth_service import AuthService
from src.services.book_service import BookService
from src.models.user import UserRole

def load_sample_data():
    """Load sample data into the database"""
    print("Loading sample data...")
    
    auth_service = AuthService()
    book_service = BookService()
    
    try:
        # Create admin user
        success, msg = auth_service.register_user(
            username="admin",
            email="admin@library.com",
            password="admin123",
            full_name="Admin User",
            role=UserRole.ADMIN
        )
        print(f"[Admin] {msg}")
        
        # Create librarian user
        success, msg = auth_service.register_user(
            username="librarian",
            email="librarian@library.com",
            password="librarian123",
            full_name="Librarian User",
            role=UserRole.LIBRARIAN
        )
        print(f"[Librarian] {msg}")
        
        # Create member users
        members = [
            ("john_doe", "john@example.com", "John Doe"),
            ("jane_smith", "jane@example.com", "Jane Smith"),
            ("bob_wilson", "bob@example.com", "Bob Wilson"),
        ]
        
        for username, email, full_name in members:
            success, msg = auth_service.register_user(
                username=username,
                email=email,
                password="password123",
                full_name=full_name,
                role=UserRole.MEMBER
            )
            print(f"[Member] {msg}")
        
        # Add sample books
        books = [
            ("To Kill a Mockingbird", "Harper Lee", "Fiction", "978-0-06-112008-4", 1960, "J. B. Lippincott", "A gripping tale of racial injustice", 5, 24.99),
            ("1984", "George Orwell", "Dystopian", "978-0-451-52493-2", 1949, "Secker & Warburg", "A dystopian social science fiction", 4, 13.99),
            ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "978-0-7432-7356-5", 1925, "Scribner", "A tale of the Jazz Age", 3, 10.99),
            ("Pride and Prejudice", "Jane Austen", "Romance", "978-0-14-143951-8", 1813, "T. Egerton", "A romantic novel of England", 6, 9.99),
            ("The Catcher in the Rye", "J. D. Salinger", "Fiction", "978-0-316-76948-0", 1951, "Little, Brown", "Story of teenage alienation", 3, 15.99),
            ("Wuthering Heights", "Emily Brontë", "Romance", "978-0-14-043207-1", 1847, "Thomas Cautley Newby", "A tale of passionate love", 2, 11.99),
            ("Jane Eyre", "Charlotte Brontë", "Romance", "978-0-14-143951-8", 1847, "Smith, Elder & Co", "A gothic romance novel", 4, 12.99),
            ("The Hobbit", "J. R. R. Tolkien", "Fantasy", "978-0-547-92822-8", 1937, "Allen & Unwin", "An adventure tale", 5, 14.99),
            ("The Lord of the Rings", "J. R. R. Tolkien", "Fantasy", "978-0-544-00529-8", 1954, "Allen & Unwin", "Epic fantasy series", 4, 29.99),
            ("Harry Potter and the Philosopher's Stone", "J. K. Rowling", "Fantasy", "978-0-747-53960-1", 1997, "Bloomsbury", "Young wizard's adventure", 6, 7.99),
        ]
        
        for title, author, genre, isbn, year, publisher, desc, copies, price in books:
            success, msg = book_service.add_book(
                title=title,
                author=author,
                genre=genre,
                isbn=isbn,
                publication_year=year,
                publisher=publisher,
                description=desc,
                total_copies=copies,
                price=price
            )
            print(f"[Book] {msg}")
        
        print("\nSample data loaded successfully!")
        
    except Exception as e:
        print(f"Error loading sample data: {e}")
    
    finally:
        auth_service.close()
        book_service.close()

if __name__ == "__main__":
    load_sample_data()
