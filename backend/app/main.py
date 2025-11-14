from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import os
from typing import Dict, Any, Optional
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="KC Experian API Integration",
    description="FastAPI backend for Experian contact and address search",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class SearchRequest(BaseModel):
    FIRST_NAME: str = Field(..., min_length=1, max_length=50, description="First name")
    LAST_NAME: str = Field(..., min_length=1, max_length=50, description="Last name")
    STREET1: str = Field(..., min_length=1, max_length=100, description="Street address line 1")
    STREET2: Optional[str] = Field(None, max_length=100, description="Street address line 2")
    CITY: str = Field(..., min_length=1, max_length=50, description="City")
    STATE: str = Field(..., min_length=2, max_length=2, description="State code (2 letters)")
    ZIP: str = Field(..., min_length=5, max_length=10, description="ZIP code")

class ExperianPayload(BaseModel):
    LEAD_TRANS_DETAILS: Dict[str, str]
    LEAD_ADDRESS: Dict[str, str]

# Configuration
EXPERIAN_API_URL = os.getenv("EXPERIAN_API_URL")
EXPERIAN_AUTH_TOKEN = os.getenv("EXPERIAN_AUTH_TOKEN")

# Debug logging for environment variables
print(f"DEBUG: EXPERIAN_API_URL = {EXPERIAN_API_URL}")
print(f"DEBUG: EXPERIAN_AUTH_TOKEN = {EXPERIAN_AUTH_TOKEN[:10]}...{EXPERIAN_AUTH_TOKEN[-10:] if EXPERIAN_AUTH_TOKEN else 'None'}")

def clean_response_data(data: Any) -> Any:
    """
    Recursively clean response data by removing empty, null, or blank values.
    Only returns fields that contain actual data.
    """
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            cleaned_value = clean_response_data(value)
            if cleaned_value is not None and cleaned_value != "" and cleaned_value != {}:
                cleaned[key] = cleaned_value
        return cleaned if cleaned else None
    
    elif isinstance(data, list):
        cleaned = [clean_response_data(item) for item in data]
        cleaned = [item for item in cleaned if item is not None and item != "" and item != {}]
        return cleaned if cleaned else None
    
    elif isinstance(data, str):
        return data.strip() if data.strip() else None
    
    else:
        return data if data is not None else None

def transform_to_experian_format(search_data: SearchRequest) -> ExperianPayload:
    """Transform input data to Experian API format"""
    return ExperianPayload(
        LEAD_TRANS_DETAILS={
            "FIRST_NAME": search_data.FIRST_NAME,
            "LAST_NAME": search_data.LAST_NAME
        },
        LEAD_ADDRESS={
            "STREET1": search_data.STREET1,
            "STREET2": search_data.STREET2 or "",
            "CITY": search_data.CITY,
            "STATE": search_data.STATE.upper(),
            "ZIP": search_data.ZIP
        }
    )

@app.post("/search")
async def search_experian(search_request: SearchRequest):
    """
    Search Experian database for contact and address information
    """
    try:
        # Transform input to Experian format
        experian_payload = transform_to_experian_format(search_request)
        
        # Prepare headers for Experian API
        headers = {
            "Auth-Token": EXPERIAN_AUTH_TOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Make request to Experian API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                EXPERIAN_API_URL,
                json=experian_payload.dict(),
                headers=headers
            )
            
            # Check if request was successful
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Experian API error: {response.text}"
                )
            
            # Parse response
            experian_data = response.json()
            
            # Clean the response data
            cleaned_data = clean_response_data(experian_data)
            
            if not cleaned_data:
                return {"message": "No data found for the provided search criteria"}
            
            return cleaned_data
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="Request to Experian API timed out"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error connecting to Experian API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "KC Experian API Integration",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "experian-api-integration"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "localhost")
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )