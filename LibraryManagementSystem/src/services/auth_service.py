"""
Authentication Service
"""
from src.database.config import SessionLocal
from src.models import User
from src.models.user import UserRole
from src.utils.auth import set_current_user, logout as auth_logout
import sys

class AuthService:
    def __init__(self):
        self.session = SessionLocal()
    
    def register_user(self, username, email, password, full_name, phone=None, address=None, role=UserRole.MEMBER):
        """Register a new user"""
        try:
            # Check if username or email already exists
            existing_user = self.session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                return False, "Username or email already exists!"
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone,
                address=address,
                role=role
            )
            new_user.set_password(password)
            
            self.session.add(new_user)
            self.session.commit()
            return True, f"User '{username}' registered successfully!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error registering user: {str(e)}"
    
    def login(self, username, password):
        """Login user"""
        try:
            user = self.session.query(User).filter(User.username == username).first()
            
            if not user:
                return False, "User not found!"
            
            if not user.is_active:
                return False, "User account is inactive!"
            
            if not user.verify_password(password):
                return False, "Incorrect password!"
            
            set_current_user(user)
            return True, f"Welcome, {user.full_name}!"
        
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def logout(self):
        """Logout current user"""
        auth_logout()
        return True, "Logged out successfully!"
    
    def change_password(self, user_id, old_password, new_password):
        """Change password for a user"""
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return False, "User not found!"
            
            if not user.verify_password(old_password):
                return False, "Old password is incorrect!"
            
            user.set_password(new_password)
            self.session.commit()
            return True, "Password changed successfully!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error changing password: {str(e)}"
    
    def reset_password(self, username, new_password):
        """Reset password (admin only)"""
        try:
            user = self.session.query(User).filter(User.username == username).first()
            
            if not user:
                return False, "User not found!"
            
            user.set_password(new_password)
            self.session.commit()
            return True, f"Password reset for user '{username}'!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error resetting password: {str(e)}"
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self):
        """Get all users"""
        return self.session.query(User).all()
    
    def deactivate_user(self, user_id):
        """Deactivate a user account"""
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found!"
            
            user.is_active = 0
            self.session.commit()
            return True, f"User account deactivated!"
        
        except Exception as e:
            self.session.rollback()
            return False, f"Error deactivating user: {str(e)}"
    
    def close(self):
        """Close database session"""
        self.session.close()
