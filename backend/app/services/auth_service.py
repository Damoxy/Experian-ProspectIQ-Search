"""
Authentication service for user management
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from database import User, PasswordResetToken
from models import UserCreate, UserLogin, UserResponse
from auth import get_password_hash, verify_password
from typing import Optional
import secrets
from datetime import datetime, timedelta

class AuthService:
    """Service class for user authentication operations"""
    
    def create_user(self, db: Session, user: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    def authenticate_user_detailed(self, db: Session, email: str, password: str) -> tuple[Optional[User], str]:
        """Authenticate user with detailed error information"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None, "EMAIL_NOT_FOUND"
        if not verify_password(password, user.hashed_password):
            return None, "INCORRECT_PASSWORD"
        return user, "SUCCESS"
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def user_to_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse"""
        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            is_active=user.is_active
        )
    
    def create_password_reset_token(self, db: Session, email: str) -> Optional[str]:
        """Create a password reset token for the user"""
        user = self.get_user_by_email(db, email)
        if not user:
            # Don't reveal whether the email exists or not for security
            return None
        
        # Generate a secure random token
        token = secrets.token_urlsafe(32)
        
        # Set expiration time (1 hour from now)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        # Create reset token record
        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        
        db.add(reset_token)
        db.commit()
        
        return token
    
    def reset_password_with_token(self, db: Session, token: str, new_password: str) -> bool:
        """Reset password using a valid token"""
        # Find the token
        reset_token = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).first()
        
        if not reset_token:
            return False
        
        # Get the user
        user = db.query(User).filter(User.id == reset_token.user_id).first()
        if not user:
            return False
        
        # Update password and updated_at timestamp
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        # Mark token as used
        reset_token.used = True
        
        db.commit()
        return True
    
    def reset_password_by_email(self, db: Session, email: str, new_password: str) -> bool:
        """Reset password directly using email address"""
        user = self.get_user_by_email(db, email)
        if not user:
            return False
        
        # Update password and updated_at timestamp
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()
        return True

# Create a single instance to use across the application
auth_service = AuthService()