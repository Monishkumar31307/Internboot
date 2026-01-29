# Library Management System - Project Documentation

## Overview
A comprehensive database-driven Library Management System built with Python and MySQL.

## Features

### 1. Search and Filtering
- Search books by title, author, genre
- Filter by availability status
- Advanced search with multiple criteria
- ISBN lookup

### 2. Borrowing & Returning
- Borrow books with automatic due date assignment
- Return books with fine calculation
- Renew books for additional time
- Track borrowing history

### 3. User Authentication & Authorization
- Role-based access control (Admin, Librarian, Member)
- User registration and login
- Password management
- User profile management

### 4. Fine Management
- Automatic fine calculation for overdue books
- Fine payment tracking
- Fine waiver functionality (admin)

### 5. Reports & Analytics
- Popular books report
- Overdue books report
- Inventory status report
- Fine statistics report
- Export to CSV

## Project Structure

```
LibraryManagementSystem/
├── src/
│   ├── database/
│   │   ├── config.py           # Database configuration
│   │   ├── schema.py           # Schema creation
│   │   └── __init__.py
│   ├── models/
│   │   ├── user.py             # User model
│   │   ├── book.py             # Book model
│   │   ├── transaction.py       # Borrow/Return transactions
│   │   ├── fine.py             # Fine model
│   │   └── __init__.py
│   ├── services/
│   │   ├── auth_service.py          # Authentication
│   │   ├── book_service.py          # Book management
│   │   ├── borrow_service.py        # Borrowing logic
│   │   ├── report_service.py        # Reports
│   │   ├── fine_service.py          # Fine management
│   │   └── __init__.py
│   ├── utils/
│   │   ├── auth.py             # Auth decorators
│   │   └── __init__.py
│   └── __init__.py
├── data/
│   └── reports/                # Generated reports
├── main.py                     # Main CLI application
├── setup.py                    # Setup script
├── sample_data.py              # Sample data loader
├── requirements.txt            # Dependencies
├── .env                        # Configuration
└── README.md                   # This file

## Installation & Setup

### Prerequisites
- Python 3.7+
- MySQL Community Edition
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Database
Edit `.env` file with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=library_management
DB_PORT=3306
```

### Step 3: Initialize Database
```bash
python setup.py
```

This will:
- Create the database
- Create all tables
- Load sample data with test users and books

### Step 4: Run the Application
```bash
python main.py
```

## Usage

### Default Test Users
- **Admin Account**: 
  - Username: `admin`
  - Password: `admin123`

- **Librarian Account**: 
  - Username: `librarian`
  - Password: `librarian123`

- **Member Accounts**: 
  - Username: `john_doe`, `jane_smith`, `bob_wilson`
  - Password: `password123`

### User Roles & Features

#### Admin
- Manage all users
- Manage all books
- View comprehensive reports
- Reset user passwords
- Deactivate user accounts

#### Librarian
- Add, update, delete books
- Manage borrowing and returns
- Process book renewals
- View reports
- Monitor overdue books

#### Member
- Search and browse library books
- Borrow and return books
- Renew borrowed books
- View personal fines
- Check borrowing history

## Database Schema

### Users Table
- id, username, email, password_hash, full_name, role, phone, address, created_at, updated_at, is_active

### Books Table
- id, title, author, genre, isbn, publication_year, publisher, description, total_copies, available_copies, price, created_at, updated_at

### Transactions Table
- id, user_id, book_id, transaction_type, borrow_date, due_date, return_date, status, notes

### Fines Table
- id, transaction_id, user_id, amount, reason, status, issued_date, paid_date, notes

## Key Features Details

### Search & Filter
- Full-text search on title, author, genre
- Filter by availability
- Combine multiple search criteria
- View all books or available only

### Borrowing Logic
- Max 5 books per user
- Default 14-day borrow period
- Automatic due date calculation
- One-click renewal

### Fine System
- $5 per day overdue
- Automatic calculation on return
- Pending/Paid/Waived status tracking
- Admin can waive fines

### Reports
- CSV export format
- Timestamps on exports
- Export to `data/reports/` folder
- Sortable data

## Technical Stack
- **Backend**: Python 3.7+
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: Custom session-based
- **CSV Export**: Python built-in csv module
- **Architecture**: Service-oriented architecture

## Learning Outcomes Met
✓ Relational database design with normalization
✓ SQL query optimization with SQLAlchemy ORM
✓ Multi-tier application architecture
✓ Role-based access control implementation
✓ Transaction management and ACID principles
✓ Error handling and data validation
✓ Report generation and data export
✓ Backend application best practices

## Troubleshooting

### "Connection refused" error
- Ensure MySQL server is running
- Check %s in .env file
- Verify DB_HOST is correct (localhost for local MySQL)

### "Table already exists" error
- Database was already initialized
- Delete tables manually or drop and recreate database

### Import errors
- Run `pip install -r requirements.txt` again
- Ensure you're in virtual environment if using one

## Future Enhancements
- Web UI with Flask/Django
- Advanced reporting with PDF export
- Email notifications for overdue books
- Book reservation system
- Mobile app support
- Advanced analytics and dashboards

## License
This project is created for educational purposes.

## Support
For issues or questions, refer to the code documentation and comments throughout the project.
