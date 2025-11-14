"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Dict, Optional

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