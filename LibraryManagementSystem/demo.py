"""
DEMO MODE - Testing the application without MySQL
This demonstrates all the features of the Library Management System
"""
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("  LIBRARY MANAGEMENT SYSTEM - DEMO MODE")
print("  (Testing without MySQL connection)")
print("="*70)

# Sample data structures for demo
demo_users = [
    {"id": 1, "username": "admin", "full_name": "Admin User", "role": "admin"},
    {"id": 2, "username": "librarian", "full_name": "Librarian User", "role": "librarian"},
    {"id": 3, "username": "john_doe", "full_name": "John Doe", "role": "member"},
]

demo_books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "available": 5},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "available": 4},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "available": 3},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "available": 6},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J. D. Salinger", "genre": "Fiction", "available": 3},
]

demo_transactions = [
    {"id": 1, "user": "john_doe", "book": "To Kill a Mockingbird", "status": "active", "days_left": 5},
    {"id": 2, "user": "jane_smith", "book": "1984", "status": "active", "days_left": 10},
]

demo_fines = [
    {"id": 1, "user": "bob_wilson", "amount": 25, "reason": "Overdue by 5 days", "status": "pending"},
]

def display_menu():
    """Display main menu"""
    print("\n" + "-"*70)
    print("DEMO APPLICATION MENU")
    print("-"*70)
    print("1. View All Users")
    print("2. View All Books")
    print("3. Search Books")
    print("4. View Transactions (Borrowed Books)")
    print("5. View Fines")
    print("6. View Database Structure")
    print("7. Setup Instructions")
    print("8. EXIT")
    print("-"*70)

def view_users():
    """Display all users"""
    print("\n[ALL USERS]")
    print(f"{'ID':<5} {'Username':<20} {'Full Name':<25} {'Role':<15}")
    print("-" * 65)
    for user in demo_users:
        print(f"{user['id']:<5} {user['username']:<20} {user['full_name']:<25} {user['role']:<15}")

def view_books():
    """Display all books"""
    print("\n[ALL BOOKS (Sample Data)]")
    print(f"{'ID':<5} {'Title':<35} {'Author':<20} {'Genre':<15} {'Available':<10}")
    print("-" * 85)
    for book in demo_books:
        status = f"{book['available']} copies"
        print(f"{book['id']:<5} {book['title'][:33]:<35} {book['author'][:18]:<20} {book['genre']:<15} {status:<10}")

def search_books():
    """Search books"""
    print("\n[SEARCH BOOKS]")
    query = input("Enter book title to search: ").strip().lower()
    
    results = [b for b in demo_books if query in b['title'].lower()]
    
    if results:
        print(f"\nFound {len(results)} book(s):")
        print(f"{'ID':<5} {'Title':<35} {'Author':<20} {'Available':<10}")
        print("-" * 70)
        for book in results:
            print(f"{book['id']:<5} {book['title'][:33]:<35} {book['author'][:18]:<20} {book['available']:<10}")
    else:
        print(f"No books found matching '{query}'")

def view_transactions():
    """Display borrowed books"""
    print("\n[BORROWED BOOKS]")
    print(f"{'Trans ID':<10} {'User':<20} {'Book':<35} {'Status':<10} {'Days Left':<10}")
    print("-" * 85)
    for trans in demo_transactions:
        print(f"{trans['id']:<10} {trans['user']:<20} {trans['book'][:33]:<35} {trans['status']:<10} {trans['days_left']:<10}")

def view_fines():
    """Display fines"""
    print("\n[FINES]")
    print(f"{'Fine ID':<10} {'User':<20} {'Amount':<10} {'Reason':<35} {'Status':<10}")
    print("-" * 85)
    for fine in demo_fines:
        print(f"{fine['id']:<10} {fine['user']:<20} ₹{fine['amount']:<9} {fine['reason'][:33]:<35} {fine['status']:<10}")

def view_structure():
    """Display database structure"""
    print("\n[DATABASE STRUCTURE]")
    print("\n1. USERS TABLE")
    print("   - id, username, email, password_hash, full_name, role")
    print("   - phone, address, created_at, updated_at, is_active")
    print("   - Roles: admin, librarian, member")
    
    print("\n2. BOOKS TABLE")
    print("   - id, title, author, genre, isbn, publication_year")
    print("   - publisher, description, total_copies, available_copies")
    print("   - price, created_at, updated_at")
    
    print("\n3. TRANSACTIONS TABLE")
    print("   - id, user_id, book_id, transaction_type")
    print("   - borrow_date, due_date, return_date, status, notes")
    print("   - Status: active, completed, overdue")
    
    print("\n4. FINES TABLE")
    print("   - id, transaction_id, user_id, amount, reason")
    print("   - status, issued_date, paid_date, notes")
    print("   - Status: pending, paid, waived")

def view_setup_instructions():
    """Display setup instructions"""
    print("\n" + "="*70)
    print("SETUP INSTRUCTIONS - TO USE WITH REAL MySQL DATABASE")
    print("="*70)
    
    print("\n📝 STEP 1: INSTALL DEPENDENCIES")
    print("   cd C:\\Users\\monis\\Downloads\\internboot\\LibraryManagementSystem")
    print("   pip install -r requirements.txt")
    print("   ✓ Already done!")
    
    print("\n📝 STEP 2: INSTALL & START MySQL")
    print("   Option A: Download from mysql.com")
    print("   Option B: If installed, start service:")
    print("            Windows: Services.msc → MySQL80 → Start")
    print("            Or: net start MySQL80 (as Admin)")
    
    print("\n📝 STEP 3: CONFIGURE .env FILE")
    print("   Edit: .env file")
    print("   Set your MySQL credentials:")
    print("   - DB_HOST=localhost")
    print("   - DB_USER=root")
    print("   - DB_PASSWORD=your_mysql_password")
    print("   - DB_NAME=library_management")
    print("   - DB_PORT=3306")
    
    print("\n📝 STEP 4: RUN SETUP (one time)")
    print("   python setup.py")
    print("   This will:")
    print("   - Create database")
    print("   - Create all tables")
    print("   - Load sample data")
    
    print("\n📝 STEP 5: RUN APPLICATION")
    print("   python main.py")
    print("   Then login with:")
    print("   - Username: admin | Password: admin123")
    print("   - Username: librarian | Password: librarian123")
    print("   - Username: john_doe | Password: password123")
    
    print("\n" + "="*70)

def main():
    """Main demo loop"""
    running = True
    
    while running:
        display_menu()
        choice = input("Select option (1-8): ").strip()
        
        if choice == "1":
            view_users()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_books()
        elif choice == "4":
            view_transactions()
        elif choice == "5":
            view_fines()
        elif choice == "6":
            view_structure()
        elif choice == "7":
            view_setup_instructions()
        elif choice == "8":
            print("\n✓ Thank you for testing Library Management System!")
            print("  When ready with MySQL, run: python main.py")
            running = False
        else:
            print("❌ Invalid option! Please select 1-8")

if __name__ == "__main__":
    main()
