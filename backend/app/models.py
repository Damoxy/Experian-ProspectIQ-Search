"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Dict, Optional
from datetime import datetime

# Authentication Models
class UserCreate(BaseModel):
    """Model for user registration"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    first_name: str = Field(..., min_length=1, max_length=50, description="First name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Last name")

class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserResponse(BaseModel):
    """Model for user response (excluding password)"""
    id: int
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    is_active: bool = True

class Token(BaseModel):
    """Model for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ResetPasswordRequest(BaseModel):
    """Model for password reset request"""
    email: EmailStr = Field(..., description="User email address")
    new_password: str = Field(..., min_length=6, description="New password")

class SearchRequest(BaseModel):
    """Request model for Experian search"""
    FIRST_NAME: str = Field(..., min_length=1, max_length=50, description="First name")
    LAST_NAME: str = Field(..., min_length=1, max_length=50, description="Last name")
    STREET1: str = Field(..., min_length=1, max_length=100, description="Street address line 1")
    STREET2: Optional[str] = Field(None, max_length=100, description="Street address line 2")
    CITY: str = Field(..., min_length=1, max_length=50, description="City")
    STATE: str = Field(..., min_length=2, max_length=2, description="State code (2 letters)")
    ZIP: str = Field(..., min_length=5, max_length=10, description="ZIP code")

class ExperianPayload(BaseModel):
    """Payload model for Experian API"""
    LEAD_TRANS_DETAILS: Dict[str, str]
    LEAD_ADDRESS: Dict[str, str]