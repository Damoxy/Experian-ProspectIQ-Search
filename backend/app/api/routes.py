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
from services.knowledgecore_service import KnowledgeCoreService
from core.logging_config import setup_logging, log_api_request, log_api_response
from config import DEBUG
from auth import get_current_user_id
from database import get_experian_db, get_givingtrend_db

# Initialize logging
logger = setup_logging(DEBUG)

router = APIRouter()
experian_service = ExperianService()
kc_service = KnowledgeCoreService()
security = HTTPBearer()

@router.post("/search")
async def search_with_database_fallback(
    search_request: SearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    experian_db: Session = Depends(get_experian_db),
    givingtrend_db: Session = Depends(get_givingtrend_db)
):
    """
    Search with database-first approach: Check KnowledgeCore database first, 
    then fall back to Experian API if no records found
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Authenticated search request from user ID: {user_id}")
    
    # Log incoming request
    log_api_request(logger, "/search", search_request.dict())
    
    try:
        # Step 1: Search GivingTrend database first
        logger.info("Searching GivingTrend database first...")
        database_results = await kc_service.search_donors(search_request, givingtrend_db)
        
        if database_results:
            # Found records in database - return formatted response
            logger.info(f"Found {len(database_results)} records in GivingTrend database")
            result = kc_service.format_consumer_behavior_response(database_results, search_request)
            
            # Log successful completion
            total_time = time.time() - start_time
            response_json = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
            log_api_response(logger, "/search", 200, len(response_json))
            logger.info(f"Database search completed successfully in {total_time:.2f} seconds")
            
            return result
        
        # Step 2: No records found in database - fall back to Experian API
        logger.info("No records found in GivingTrend database, falling back to Experian API...")
        result = await experian_service.search(search_request)
        
        # Add source indicator to show this came from Experian fallback
        if isinstance(result, dict):
            result["fallback_source"] = "experian_api"
            result["database_checked"] = True
            result["database_records_found"] = 0
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        log_api_response(logger, "/search", 200, len(response_json))
        logger.info(f"Fallback search completed successfully in {total_time:.2f} seconds")
        
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