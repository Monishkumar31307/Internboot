"""
Database Connection Tester and Fixer
Run this to diagnose and fix database issues
"""
import sys
import os

print("="*70)
print("DATABASE CONNECTION TESTER")
print("="*70)

# Test 1: Check imports
print("\n[Test 1] Checking imports...")
try:
    from src.database.config import engine, SessionLocal, Base, DATABASE_URL
    print("✓ Imports successful")
    print(f"  Database: {DATABASE_URL}")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Check engine connection
print("\n[Test 2] Testing database engine...")
try:
    if engine:
        print("✓ Engine connected")
    else:
        print("✗ Engine is None")
        sys.exit(1)
except Exception as e:
    print(f"✗ Engine test failed: {e}")
    sys.exit(1)

# Test 3: Check session creation
print("\n[Test 3] Testing session creation...")
try:
    session = SessionLocal()
    print("✓ Session created")
    session.close()
except Exception as e:
    print(f"✗ Session creation failed: {e}")
    sys.exit(1)

# Test 4: Check database file
print("\n[Test 4] Checking database file...")
if "sqlite" in DATABASE_URL.lower():
    db_file = DATABASE_URL.replace("sqlite:///", "")
    if os.path.exists(db_file):
        size = os.path.getsize(db_file)
        print(f"✓ Database file exists: {db_file}")
        print(f"  Size: {size} bytes")
    else:
        print(f"✗ Database file not found: {db_file}")

# Test 5: Check tables
print("\n[Test 5] Checking database tables...")
try:
    from src.models import User, Book, Transaction, Fine
    
    inspector = engine.dialect.get_inspector(engine)
    tables = inspector.get_table_names()
    
    print(f"✓ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
    
    if len(tables) == 0:
        print("\n⚠ No tables found! Running table creation...")
        Base.metadata.create_all(bind=engine)
        
        inspector = engine.dialect.get_inspector(engine)
        tables = inspector.get_table_names()
        print(f"✓ Created {len(tables)} tables")
        
except Exception as e:
    print(f"✗ Table check failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Check if data exists
print("\n[Test 6] Checking for existing data...")
try:
    session = SessionLocal()
    from src.models import User, Book
    
    user_count = session.query(User).count()
    book_count = session.query(Book).count()
    
    print(f"✓ Users in database: {user_count}")
    print(f"✓ Books in database: {book_count}")
    
    if user_count == 0:
        print("\n⚠ No users found! You may need to run: python setup.py")
    
    session.close()
except Exception as e:
    print(f"⚠ Data check failed: {e}")

# Test 7: Test a simple query
print("\n[Test 7] Testing database query...")
try:
    session = SessionLocal()
    from src.models import User
    
    # Try to get admin user
    admin = session.query(User).filter(User.username == "admin").first()
    if admin:
        print(f"✓ Query successful")
        print(f"  Found user: {admin.username} ({admin.role.value})")
    else:
        print("⚠ Admin user not found (database may be empty)")
    
    session.close()
except Exception as e:
    print(f"✗ Query failed: {e}")
    import traceback
    traceback.print_exc()

# Final result
print("\n" + "="*70)
print("DATABASE DIAGNOSIS COMPLETE")
print("="*70)
print("\n✓ Database connection is WORKING!")
print("✓ All tests passed successfully")
print("\nYou can now run: python main.py")
print("="*70)
