"""
Authentication and authorization utilities
"""
from functools import wraps
import hashlib
from datetime import datetime, timedelta
import os

current_user = None  # Global variable to track current logged-in user

def login_required(func):
    """Decorator to check if user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user:
            print("Error: Please login first!")
            return None
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    """Decorator to check if user is admin"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user:
            print("Error: Please login first!")
            return None
        if current_user.role.value != "admin":
            print("Error: Admin access required!")
            return None
        return func(*args, **kwargs)
    return wrapper

def librarian_or_admin_required(func):
    """Decorator to check if user is librarian or admin"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user:
            print("Error: Please login first!")
            return None
        if current_user.role.value not in ["admin", "librarian"]:
            print("Error: Librarian or Admin access required!")
            return None
        return func(*args, **kwargs)
    return wrapper

def set_current_user(user):
    """Set the current logged-in user"""
    global current_user
    current_user = user

def get_current_user():
    """Get the current logged-in user"""
    return current_user

def logout():
    """Logout the current user"""
    global current_user
    current_user = None
