"""
Authentication API routes for login, signup, and user management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_experian_db
from models import UserCreate, UserLogin, Token, UserResponse, ResetPasswordRequest
from services.auth_service import AuthService
from auth import create_access_token, get_current_user_id, ACCESS_TOKEN_EXPIRE_MINUTES
from core.logging_config import setup_logging
from config import DEBUG

# Initialize logging
logger = setup_logging(DEBUG)

router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()
security = HTTPBearer()

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_experian_db)):
    """Register a new user"""
    try:
        logger.info(f"New user signup attempt: {user.email}")
        
        # Create user
        db_user = auth_service.create_user(db, user)
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, 
            expires_delta=access_token_expires
        )
        
        user_response = auth_service.user_to_response(db_user)
        
        logger.info(f"User created successfully: {user.email}")
        return Token(access_token=access_token, user=user_response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during signup"
        )

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_experian_db)):
    """Authenticate user and return access token"""
    try:
        logger.info(f"Login attempt for: {user.email}")
        
        # Authenticate user with detailed error info
        db_user, auth_result = auth_service.authenticate_user_detailed(db, user.email, user.password)
        if not db_user:
            logger.warning(f"Failed login attempt for: {user.email} - {auth_result}")
            if auth_result == "EMAIL_NOT_FOUND":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Email address not found"
                )
            elif auth_result == "INCORRECT_PASSWORD":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication failed"
                )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, 
            expires_delta=access_token_expires
        )
        
        user_response = auth_service.user_to_response(db_user)
        
        logger.info(f"User logged in successfully: {user.email}")
        return Token(access_token=access_token, user=user_response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_experian_db)
):
    """Get current user information"""
    try:
        user_id = get_current_user_id(credentials.credentials)
        user = auth_service.get_user_by_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return auth_service.user_to_response(user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting user information"
        )

@router.post("/forgot-password")
async def forgot_password(request: ResetPasswordRequest, db: Session = Depends(get_experian_db)):
    """Reset password directly with email and new password"""
    try:
        logger.info(f"Password reset requested for: {request.email}")
        
        # Reset password directly
        success = auth_service.reset_password_by_email(db, request.email, request.new_password)
        
        if not success:
            logger.warning(f"Password reset failed - email not found: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email address not found"
            )
        
        logger.info(f"Password reset successful for: {request.email}")
        return {"message": "Password has been reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while resetting the password"
        )
