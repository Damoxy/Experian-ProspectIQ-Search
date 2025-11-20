"""
API router for Experian search endpoints with comprehensive logging
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import json
import time

from models import SearchRequest
from services.experian_service import ExperianService
from core.logging_config import setup_logging, log_api_request, log_api_response
from config import DEBUG
from auth import get_current_user_id
from database import get_db

# Initialize logging
logger = setup_logging(DEBUG)

router = APIRouter()
experian_service = ExperianService()
security = HTTPBearer()

@router.post("/search")
async def search_experian(
    search_request: SearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Search Experian database for contact and address information
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Authenticated search request from user ID: {user_id}")
    
    # Log incoming request
    log_api_request(logger, "/search", search_request.dict())
    
    try:
        result = await experian_service.search(search_request)
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        log_api_response(logger, "/search", 200, len(response_json))
        logger.info(f"Search completed successfully in {total_time:.2f} seconds")
        
        return result
    except HTTPException:
        # Re-raise HTTP exceptions without additional logging (already logged in service)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/")
async def root():
    """Root endpoint with API information"""
    log_api_request(logger, "/", {})
    response = {
        "message": "KC Experian API Integration",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search",
            "health": "/health"
        }
    }
    log_api_response(logger, "/", 200, len(json.dumps(response)))
    return response

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    log_api_request(logger, "/health", {})
    logger.debug("Health check requested")
    response = {"status": "healthy", "service": "experian-api-integration"}
    log_api_response(logger, "/health", 200, len(json.dumps(response)))
    return response