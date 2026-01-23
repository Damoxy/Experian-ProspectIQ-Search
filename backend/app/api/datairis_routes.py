"""
DataIris API routes for prospect searching
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import json
import time

from models import SearchRequest
from datairis_service import DataIrisService
from datairis_field_mappings import transform_datairis_results
from core.logging_config import setup_logging, log_api_request, log_api_response
from config import DEBUG
from auth import get_current_user_id
from database import get_experian_db

# Initialize logging
logger = setup_logging(DEBUG)

router = APIRouter()
security = HTTPBearer()


@router.post("/datairis/search")
async def search_datairis(
    search_request: SearchRequest,
    db: Session = Depends(get_experian_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Search DataIris API for prospect information
    Takes first name, last name, and zip code to retrieve comprehensive prospect data
    (Protected endpoint - requires authentication)
    Results are cached for 90 days to reduce API calls
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Authenticated DataIris search request from user ID: {user_id}")
    
    # Log incoming request
    request_data = {
        "first_name": search_request.FIRST_NAME,
        "last_name": search_request.LAST_NAME,
        "zip_code": search_request.ZIP
    }
    log_api_request(logger, "/datairis/search", request_data)
    
    try:
        logger.info(f"Starting DataIris search for: {search_request.FIRST_NAME} {search_request.LAST_NAME}, {search_request.ZIP}")
        
        # Initialize DataIris service with database session for caching
        datairis_service = DataIrisService(db_session=db)
        
        # Perform search (will check cache first, then call API, then save to cache)
        result = datairis_service.search(
            first_name=search_request.FIRST_NAME,
            last_name=search_request.LAST_NAME,
            zip_code=search_request.ZIP,
            start=1,
            end=10
        )
        
        if not result:
            logger.warning(f"No results found from DataIris for: {search_request.FIRST_NAME} {search_request.LAST_NAME}, {search_request.ZIP}")
            return {
                "status": "success",
                "results": [],
                "record_count": 0,
                "message": "No records found matching search criteria"
            }
        
        # Extract search_response and transformed_results from result
        raw_results = result.get("search_response")
        organized_results = result.get("transformed_results", {})
        
        # Get record count from raw results
        record_count = 0
        if raw_results and isinstance(raw_results, dict):
            record_count = raw_results.get("totalCount", 0)
        
        logger.info(f"DataIris search returned {record_count} records")
        
        # Prepare response
        response = {
            "status": "success",
            "record_count": record_count,
            "results": organized_results
        }
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(response) if isinstance(response, (dict, list)) else str(response)
        log_api_response(logger, "/datairis/search", 200, len(response_json))
        logger.info(f"DataIris search completed successfully in {total_time:.2f} seconds")
        
        return response
        
    except Exception as e:
        logger.error(f"DataIris search failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"DataIris search failed: {str(e)}"
        )


@router.get("/datairis/health")
async def datairis_health(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Check DataIris API health and authentication status
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"DataIris health check request from user ID: {user_id}")
    
    try:
        logger.info("Checking DataIris API health...")
        
        # Initialize DataIris service (no caching needed for health check)
        datairis_service = DataIrisService()
        
        # Try to authenticate
        token_id = datairis_service.authenticate()
        
        if not token_id:
            logger.error("DataIris authentication failed")
            return {
                "status": "error",
                "message": "Failed to authenticate with DataIris API",
                "authenticated": False
            }
        
        logger.info("DataIris API authentication successful")
        
        response = {
            "status": "healthy",
            "authenticated": True,
            "message": "DataIris API is accessible and authenticated"
        }
        
        total_time = time.time() - start_time
        log_api_response(logger, "/datairis/health", 200, len(json.dumps(response)))
        
        return response
        
    except Exception as e:
        logger.error(f"DataIris health check failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}",
            "authenticated": False
        }
