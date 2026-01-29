"""
Setup and Installation Guide for Library Management System
Run this script to set up the database and load sample data
"""
from src.database.schema import initialize_database
from sample_data import load_sample_data
import sys

def setup():
    """Complete setup process"""
    print("=" * 60)
    print("LIBRARY MANAGEMENT SYSTEM - SETUP")
    print("=" * 60)
    
    # Step 1: Initialize database
    print("\n[Step 1/2] Initializing Database...")
    if not initialize_database():
        print("✗ Failed to initialize database!")
        print("Make sure MySQL is running and credentials in .env are correct")
        sys.exit(1)
    
    # Step 2: Load sample data
    print("\n[Step 2/2] Loading Sample Data...")
    try:
        load_sample_data()
        print("\n✓ Setup completed successfully!")
        print("\nYou can now run: python main.py")
    except Exception as e:
        print(f"✗ Error loading sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup()
