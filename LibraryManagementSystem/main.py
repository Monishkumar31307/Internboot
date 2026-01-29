"""
Main Command Line Interface for Library Management System
"""
from src.services.auth_service import AuthService
from src.services.book_service import BookService
from src.services.borrow_service import BorrowService
from src.services.report_service import ReportService
from src.services.fine_service import FineService
from src.utils.auth import get_current_user, login_required, admin_required, librarian_or_admin_required
from src.database.schema import initialize_database
from src.models.user import UserRole
import sys
from datetime import datetime

class LibraryManagementApp:
    def __init__(self):
        self.running = True
        self.auth_service = AuthService()
        self.book_service = BookService()
        self.borrow_service = BorrowService()
        self.report_service = ReportService()
        self.fine_service = FineService()
    
    def display_header(self):
        """Display application header"""
        print("\n" + "="*60)
        print("      LIBRARY MANAGEMENT SYSTEM")
        print("="*60)
    
    def display_main_menu(self):
        """Display main menu"""
        self.display_header()
        current_user = get_current_user()
        
        if current_user:
            print(f"Logged in as: {current_user.full_name} ({current_user.role.value})")
            print("-" * 60)
            
            if current_user.role == UserRole.ADMIN:
                print("\n[ADMIN MENU]")
                print("1. Manage Users")
                print("2. Manage Books")
                print("3. View Reports")
                print("4. Logout")
                print("5. Exit")
            elif current_user.role == UserRole.LIBRARIAN:
                print("\n[LIBRARIAN MENU]")
                print("1. Manage Books")
                print("2. Manage Borrowing/Returns")
                print("3. View Reports")
                print("4. Logout")
                print("5. Exit")
            else:  # Member
                print("\n[MEMBER MENU]")
                print("1. Search Books")
                print("2. Borrow Book")
                print("3. Return Book")
                print("4. My Books")
                print("5. My Fines")
                print("6. Pay Fines")
                print("7. Logout")
                print("8. Exit")
        else:
            print("\n[LOGIN MENU]")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
    
    def handle_admin_menu(self):
        """Handle admin menu"""
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            self.manage_users()
        elif choice == "2":
            self.manage_books()
        elif choice == "3":
            self.view_reports()
        elif choice == "4":
            self.logout()
        elif choice == "5":
            self.exit_app()
    
    def handle_librarian_menu(self):
        """Handle librarian menu"""
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            self.manage_books()
        elif choice == "2":
            self.manage_borrowing()
        elif choice == "3":
            self.view_reports()
        elif choice == "4":
            self.logout()
        elif choice == "5":
            self.exit_app()
    
    def handle_member_menu(self):
        """Handle member menu"""
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            self.search_books()
        elif choice == "2":
            self.member_borrow_book()
        elif choice == "3":
            self.member_return_book()
        elif choice == "4":
            self.view_my_books()
        elif choice == "5":
            self.view_my_fines()
        elif choice == "6":
            self.member_pay_fines()
        elif choice == "7":
            self.logout()
        elif choice == "8":
            self.exit_app()
    
    def handle_login_menu(self):
        """Handle login menu"""
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            self.exit_app()
    
    # ==== AUTHENTICATION METHODS ====
    
    def login(self):
        """Login user"""
        print("\n[LOGIN]")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        success, message = self.auth_service.login(username, password)
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    
    def register(self):
        """Register new user"""
        print("\n[REGISTER]")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        full_name = input("Full Name: ").strip()
        phone = input("Phone (optional): ").strip()
        address = input("Address (optional): ").strip()
        
        success, message = self.auth_service.register_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            phone=phone if phone else None,
            address=address if address else None,
            role=UserRole.MEMBER
        )
        
        if success:
            print(f"✓ {message}")
            self.login()
        else:
            print(f"✗ {message}")
    
    def logout(self):
        """Logout current user"""
        success, message = self.auth_service.logout()
        print(f"✓ {message}")
    
    # ==== BOOK MANAGEMENT METHODS ====
    
    def manage_books(self):
        """Manage books menu"""
        current_user = get_current_user()
        
        while True:
            print("\n[BOOK MANAGEMENT]")
            
            if current_user.role in [UserRole.ADMIN, UserRole.LIBRARIAN]:
                print("1. Add Book")
                print("2. Update Book")
                print("3. Delete Book")
                print("4. View All Books")
                print("5. Search Books")
                print("6. Back")
                
                choice = input("\nSelect option: ").strip()
                
                if choice == "1":
                    self.add_book()
                elif choice == "2":
                    self.update_book()
                elif choice == "3":
                    self.delete_book()
                elif choice == "4":
                    self.view_all_books()
                elif choice == "5":
                    self.search_books()
                elif choice == "6":
                    break
            else:
                self.search_books()
                break
    
    def add_book(self):
        """Add new book"""
        print("\n[ADD BOOK]")
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        genre = input("Genre: ").strip()
        isbn = input("ISBN: ").strip()
        pub_year = input("Publication Year (optional): ").strip()
        publisher = input("Publisher (optional): ").strip()
        description = input("Description (optional): ").strip()
        total_copies = input("Total Copies (default 1): ").strip()
        price = input("Price (optional): ").strip()
        
        success, message = self.book_service.add_book(
            title=title,
            author=author,
            genre=genre,
            isbn=isbn,
            publication_year=int(pub_year) if pub_year else None,
            publisher=publisher if publisher else None,
            description=description if description else None,
            total_copies=int(total_copies) if total_copies else 1,
            price=float(price) if price else None
        )
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    
    def update_book(self):
        """Update book details"""
        print("\n[UPDATE BOOK]")
        book_id = input("Enter Book ID: ").strip()
        
        if not book_id.isdigit():
            print("✗ Invalid Book ID!")
            return
        
        book = self.book_service.get_book_by_id(int(book_id))
        if not book:
            print("✗ Book not found!")
            return
        
        print(f"\nCurrent: {book.title} by {book.author}")
        print("1. Update Title")
        print("2. Update Author")
        print("3. Update Genre")
        print("4. Update Total Copies")
        print("5. Update Price")
        
        choice = input("\nWhat to update: ").strip()
        
        updates = {}
        if choice == "1":
            updates['title'] = input("New Title: ").strip()
        elif choice == "2":
            updates['author'] = input("New Author: ").strip()
        elif choice == "3":
            updates['genre'] = input("New Genre: ").strip()
        elif choice == "4":
            updates['total_copies'] = int(input("New Total Copies: ").strip())
        elif choice == "5":
            updates['price'] = float(input("New Price: ").strip())
        
        if updates:
            success, message = self.book_service.update_book(int(book_id), **updates)
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
    
    def delete_book(self):
        """Delete book"""
        print("\n[DELETE BOOK]")
        book_id = input("Enter Book ID to delete: ").strip()
        
        if not book_id.isdigit():
            print("✗ Invalid Book ID!")
            return
        
        book = self.book_service.get_book_by_id(int(book_id))
        if not book:
            print("✗ Book not found!")
            return
        
        confirm = input(f"Delete '{book.title}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            success, message = self.book_service.delete_book(int(book_id))
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
    
    def view_all_books(self):
        """View all books"""
        print("\n[ALL BOOKS]")
        books = self.book_service.get_all_books()
        
        if not books:
            print("No books found!")
            return
        
        print(f"{'ID':<5} {'Title':<35} {'Author':<20} {'Available':<10} {'Total':<5}")
        print("-" * 75)
        for book in books:
            print(f"{book.id:<5} {book.title[:33]:<35} {book.author[:18]:<20} {book.available_copies:<10} {book.total_copies:<5}")
    
    def search_books(self):
        """Search books"""
        print("\n[SEARCH BOOKS]")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Genre")
        print("4. View Available Books")
        print("5. Advanced Search")
        
        choice = input("\nSelect option: ").strip()
        results = []
        
        if choice == "1":
            title = input("Enter title: ").strip()
            results = self.book_service.search_by_title(title)
        elif choice == "2":
            author = input("Enter author: ").strip()
            results = self.book_service.search_by_author(author)
        elif choice == "3":
            genre = input("Enter genre: ").strip()
            results = self.book_service.search_by_genre(genre)
        elif choice == "4":
            results = self.book_service.filter_available_books()
        elif choice == "5":
            title = input("Title (optional): ").strip()
            author = input("Author (optional): ").strip()
            genre = input("Genre (optional): ").strip()
            available = input("Available only? (yes/no): ").strip().lower() == "yes"
            
            results = self.book_service.advanced_search(
                title=title if title else None,
                author=author if author else None,
                genre=genre if genre else None,
                availability=available if available else None
            )
        
        if results:
            print(f"\nFound {len(results)} book(s):")
            print(f"{'ID':<5} {'Title':<35} {'Author':<20} {'Genre':<15} {'Available':<10}")
            print("-" * 85)
            for book in results:
                print(f"{book.id:<5} {book.title[:33]:<35} {book.author[:18]:<20} {book.genre[:13]:<15} {book.available_copies:<10}")
        else:
            print("No books found!")
    
    # ==== BORROWING METHODS ====
    
    def manage_borrowing(self):
        """Manage borrowing/returns"""
        while True:
            print("\n[BORROWING MANAGEMENT]")
            print("1. Borrow Book")
            print("2. Return Book")
            print("3. Renew Book")
            print("4. View Overdue Books")
            print("5. Back")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.borrow_book_menu()
            elif choice == "2":
                self.return_book_menu()
            elif choice == "3":
                self.renew_book_menu()
            elif choice == "4":
                self.view_overdue_books()
            elif choice == "5":
                break
    
    def borrow_book_menu(self):
        """Borrow book menu"""
        print("\n[BORROW BOOK]")
        
        # Show available books
        available = self.book_service.filter_available_books()
        if available:
            print("Available Books:")
            print(f"{'ID':<5} {'Title':<35} {'Author':<20}")
            print("-" * 60)
            for book in available[:10]:  # Show first 10
                print(f"{book.id:<5} {book.title[:33]:<35} {book.author[:18]:<20}")
            
            user_id = input("\nEnter User ID: ").strip()
            book_id = input("Enter Book ID: ").strip()
            
            if user_id.isdigit() and book_id.isdigit():
                success, message = self.borrow_service.borrow_book(int(user_id), int(book_id))
                if success:
                    print(f"✓ {message}")
                else:
                    print(f"✗ {message}")
        else:
            print("No books available!")
    
    def return_book_menu(self):
        """Return book menu"""
        print("\n[RETURN BOOK]")
        transaction_id = input("Enter Transaction ID: ").strip()
        
        if transaction_id.isdigit():
            success, message = self.borrow_service.return_book(int(transaction_id))
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
    
    def renew_book_menu(self):
        """Renew book menu"""
        print("\n[RENEW BOOK]")
        transaction_id = input("Enter Transaction ID: ").strip()
        days = input("Renew for days (default 14): ").strip()
        
        if transaction_id.isdigit():
            days = int(days) if days.isdigit() else 14
            success, message = self.borrow_service.renew_book(int(transaction_id), days)
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
    
    def view_my_books(self):
        """View user's borrowed books"""
        current_user = get_current_user()
        if not current_user:
            print("✗ Please login first!")
            return
        
        print("\n[MY BOOKS]")
        books = self.borrow_service.get_user_borrowed_books(current_user.id)
        
        if not books:
            print("You have no borrowed books!")
            return
        
        print(f"\n{'Trans ID':<10} {'Book Title':<35} {'Due Date':<15} {'Days Left':<10}")
        print("-" * 70)
        for trans in books:
            days_left = (trans.due_date - datetime.utcnow()).days
            print(f"{trans.id:<10} {trans.book.title[:33]:<35} {trans.due_date.date():<15} {days_left:<10}")
    
    def view_overdue_books(self):
        """View overdue books"""
        print("\n[OVERDUE BOOKS]")
        overdue = self.borrow_service.get_overdue_transactions()
        
        if not overdue:
            print("No overdue books!")
            return
        
        print(f"\n{'Trans ID':<10} {'User':<20} {'Book Title':<35} {'Days Overdue':<15}")
        print("-" * 80)
        for trans in overdue:
            print(f"{trans.id:<10} {trans.user.full_name[:18]:<20} {trans.book.title[:33]:<35} {trans.get_days_overdue():<15}")
    
    # ==== FINES METHODS ====
    
    def view_my_fines(self):
        """View user's fines"""
        current_user = get_current_user()
        if not current_user:
            print("✗ Please login first!")
            return
        
        print("\n[MY FINES]")
        fines = self.fine_service.get_user_fines(current_user.id)
        
        if not fines:
            print("No fines!")
            return
        
        total = self.fine_service.get_total_pending_fine_amount(current_user.id)
        print(f"\n{'Fine ID':<10} {'Amount':<10} {'Reason':<35} {'Status':<10}")
        print("-" * 65)
        for fine in fines:
            print(f"{fine.id:<10} {fine.amount:<10} {fine.reason[:33]:<35} {fine.status.value:<10}")
        
        print(f"\nTotal Pending: {total}")
    
    def member_borrow_book(self):
        """Member borrow book - simplified version"""
        current_user = get_current_user()
        if not current_user:
            print("✗ Please login first!")
            return
        
        print("\n[BORROW BOOK]")
        
        # Check current borrowed books count
        current_books = self.borrow_service.get_user_borrowed_books(current_user.id)
        if len(current_books) >= 5:
            print("✗ You have reached the maximum limit of 5 borrowed books!")
            print("  Please return some books before borrowing more.")
            return
        
        # Show available books
        available = self.book_service.filter_available_books()
        if not available:
            print("No books available at the moment!")
            return
        
        print("\nAvailable Books:")
        print(f"\n{'ID':<5} {'Title':<40} {'Author':<25} {'Genre':<15}")
        print("-" * 85)
        for book in available[:20]:  # Show first 20
            print(f"{book.id:<5} {book.title[:38]:<40} {book.author[:23]:<25} {book.genre[:13]:<15}")
        
        book_id = input("\nEnter Book ID to borrow (or 'cancel'): ").strip()
        
        if book_id.lower() == 'cancel':
            return
        
        if not book_id.isdigit():
            print("✗ Invalid Book ID!")
            return
        
        success, message = self.borrow_service.borrow_book(current_user.id, int(book_id))
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    
    def member_return_book(self):
        """Member return book - simplified version"""
        current_user = get_current_user()
        if not current_user:
            print("✗ Please login first!")
            return
        
        print("\n[RETURN BOOK]")
        
        # Show user's borrowed books
        books = self.borrow_service.get_user_borrowed_books(current_user.id)
        
        if not books:
            print("You have no books to return!")
            return
        
        print("\nYour Borrowed Books:")
        print(f"\n{'Trans ID':<10} {'Book Title':<40} {'Due Date':<15} {'Days Left':<10}")
        print("-" * 75)
        for trans in books:
            days_left = (trans.due_date - datetime.utcnow()).days
            status = "OVERDUE" if days_left < 0 else f"{days_left} days"
            print(f"{trans.id:<10} {trans.book.title[:38]:<40} {trans.due_date.date():<15} {status:<10}")
        
        trans_id = input("\nEnter Transaction ID to return (or 'cancel'): ").strip()
        
        if trans_id.lower() == 'cancel':
            return
        
        if not trans_id.isdigit():
            print("✗ Invalid Transaction ID!")
            return
        
        success, message = self.borrow_service.return_book(int(trans_id))
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    
    def member_pay_fines(self):
        """Member pay fines"""
        current_user = get_current_user()
        if not current_user:
            print("✗ Please login first!")
            return
        
        print("\n[PAY FINES]")
        
        # Get pending fines
        fines = self.fine_service.get_pending_fines(current_user.id)
        
        if not fines:
            print("You have no pending fines!")
            return
        
        total = self.fine_service.get_total_pending_fine_amount(current_user.id)
        print(f"\n{'Fine ID':<10} {'Amount':<10} {'Reason':<40} {'Date':<12}")
        print("-" * 72)
        for fine in fines:
            print(f"{fine.id:<10} ₹{fine.amount:<9} {fine.reason[:38]:<40} {fine.created_at.date():<12}")
        
        print(f"\nTotal Pending Amount: ₹{total}")
        
        fine_id = input("\nEnter Fine ID to pay (or 'cancel'): ").strip()
        
        if fine_id.lower() == 'cancel':
            return
        
        if not fine_id.isdigit():
            print("✗ Invalid Fine ID!")
            return
        
        # Confirm payment
        fine = next((f for f in fines if f.id == int(fine_id)), None)
        if not fine:
            print("✗ Fine not found in your pending fines!")
            return
        
        confirm = input(f"\nPay ₹{fine.amount} for '{fine.reason}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            success, message = self.fine_service.pay_fine(int(fine_id))
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
    
    # ==== REPORTS METHODS ====
    
    def view_reports(self):
        """View reports menu"""
        print("\n[REPORTS]")
        print("1. Popular Books Report")
        print("2. Overdue Books Report")
        print("3. Inventory Status Report")
        print("4. Fine Statistics Report")
        print("5. Back")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            self.popular_books_report()
        elif choice == "2":
            self.overdue_books_report()
        elif choice == "3":
            self.inventory_report()
        elif choice == "4":
            self.fine_statistics_report()
    
    def popular_books_report(self):
        """Display and export popular books report"""
        print("\n[POPULAR BOOKS REPORT]")
        books = self.report_service.get_popular_books(10)
        
        if not books:
            print("No data available!")
            return
        
        print(f"\n{'Rank':<5} {'Title':<35} {'Author':<20} {'Times Borrowed':<15}")
        print("-" * 75)
        for i, book in enumerate(books, 1):
            print(f"{i:<5} {book[1][:33]:<35} {book[2][:18]:<20} {book[3]:<15}")
        
        export = input("\nExport to CSV? (yes/no): ").strip().lower()
        if export == "yes":
            success, message = self.report_service.export_popular_books_csv()
            print(f"✓ {message}" if success else f"✗ {message}")
    
    def overdue_books_report(self):
        """Display and export overdue books report"""
        print("\n[OVERDUE BOOKS REPORT]")
        overdue = self.report_service.get_overdue_books()
        
        if not overdue:
            print("No overdue books!")
            return
        
        print(f"\n{'ID':<5} {'User':<20} {'Email':<25} {'Book':<25} {'Days Overdue':<15}")
        print("-" * 90)
        for item in overdue:
            print(f"{item[0]:<5} {item[1][:18]:<20} {item[2][:23]:<25} {item[3][:23]:<25} {item[5]:<15}")
        
        export = input("\nExport to CSV? (yes/no): ").strip().lower()
        if export == "yes":
            success, message = self.report_service.export_overdue_books_csv()
            print(f"✓ {message}" if success else f"✗ {message}")
    
    def inventory_report(self):
        """Display and export inventory report"""
        print("\n[INVENTORY STATUS REPORT]")
        inventory = self.report_service.get_inventory_status()
        
        if not inventory:
            print("No data available!")
            return
        
        print(f"\n{'Title':<30} {'Author':<20} {'Total':<8} {'Available':<10} {'Borrowed':<10}")
        print("-" * 80)
        for item in inventory:
            print(f"{item[0][:28]:<30} {item[1][:18]:<20} {item[2]:<8} {item[3]:<10} {item[4]:<10}")
        
        export = input("\nExport to CSV? (yes/no): ").strip().lower()
        if export == "yes":
            success, message = self.report_service.export_inventory_csv()
            print(f"✓ {message}" if success else f"✗ {message}")
    
    def fine_statistics_report(self):
        """Display and export fine statistics"""
        print("\n[FINE STATISTICS REPORT]")
        stats = self.report_service.get_fine_statistics()
        
        if not stats:
            print("No data available!")
            return
        
        print(f"\n{'User':<20} {'Email':<25} {'Total Fines':<15} {'Total Amount':<15} {'Pending':<10}")
        print("-" * 85)
        for item in stats:
            print(f"{item[0][:18]:<20} {item[1][:23]:<25} {item[2]:<15} {item[3]:<15} {item[4]:<10}")
        
        export = input("\nExport to CSV? (yes/no): ").strip().lower()
        if export == "yes":
            success, message = self.report_service.export_fine_statistics_csv()
            print(f"✓ {message}" if success else f"✗ {message}")
    
    # ==== USER MANAGEMENT ====
    
    def manage_users(self):
        """Manage users (admin only)"""
        print("\n[USER MANAGEMENT]")
        print("1. View All Users")
        print("2. Reset User Password")
        print("3. Deactivate User")
        print("4. Back")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            users = self.auth_service.get_all_users()
            print(f"\n{'ID':<5} {'Username':<20} {'Email':<30} {'Role':<15} {'Active':<10}")
            print("-" * 80)
            for user in users:
                active = "Yes" if user.is_active else "No"
                print(f"{user.id:<5} {user.username:<20} {user.email:<30} {user.role.value:<15} {active:<10}")
        elif choice == "2":
            username = input("Username: ").strip()
            new_password = input("New Password: ").strip()
            success, message = self.auth_service.reset_password(username, new_password)
            print(f"✓ {message}" if success else f"✗ {message}")
        elif choice == "3":
            user_id = input("User ID: ").strip()
            if user_id.isdigit():
                success, message = self.auth_service.deactivate_user(int(user_id))
                print(f"✓ {message}" if success else f"✗ {message}")
    
    # ==== UTILITY METHODS ====
    
    def exit_app(self):
        """Exit application"""
        print("\nThank you for using Library Management System!")
        self.running = False
    
    def run(self):
        """Run the application"""
        while self.running:
            current_user = get_current_user()
            self.display_main_menu()
            
            try:
                if current_user:
                    if current_user.role == UserRole.ADMIN:
                        self.handle_admin_menu()
                    elif current_user.role == UserRole.LIBRARIAN:
                        self.handle_librarian_menu()
                    else:  # Member
                        self.handle_member_menu()
                else:
                    self.handle_login_menu()
            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.exit_app()
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.auth_service.close()
        self.book_service.close()
        self.borrow_service.close()
        self.report_service.close()
        self.fine_service.close()

def main():
    """Main entry point"""
    print("Initializing Database...")
    if not initialize_database():
        print("Failed to initialize database!")
        return
    
    app = LibraryManagementApp()
    try:
        app.run()
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()
