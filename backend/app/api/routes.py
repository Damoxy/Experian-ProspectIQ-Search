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
from services.phone_validation_service import PhoneValidationService
from services.email_validation_service import EmailValidationService
from core.logging_config import setup_logging, log_api_request, log_api_response
from config import DEBUG
from auth import get_current_user_id
from database import get_experian_db, get_givingtrend_db

# Initialize logging
logger = setup_logging(DEBUG)

router = APIRouter()
experian_service = ExperianService()
kc_service = KnowledgeCoreService()
phone_validation_service = PhoneValidationService()
email_validation_service = EmailValidationService()
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
            result = kc_service.format_consumer_behavior_response(database_results, search_request, givingtrend_db)
            
            # Add phone and email validation to database results
            try:
                logger.info("Adding phone validation to database results...")
                phone_validation_result = await phone_validation_service.validate_phone_numbers(search_request)
                if phone_validation_result and phone_validation_result.get('phone_validation'):
                    result['phone_validation'] = phone_validation_result['phone_validation']
                    logger.info("Phone validation added to database results")
            except Exception as e:
                logger.warning(f"Phone validation failed for database results: {str(e)}")
            
            try:
                logger.info("Adding email validation to database results...")
                email_validation_result = await email_validation_service.validate_email_address(search_request)
                if email_validation_result and email_validation_result.get('email_validation'):
                    result['email_validation'] = email_validation_result['email_validation']
                    logger.info("Email validation added to database results")
            except Exception as e:
                logger.warning(f"Email validation failed for database results: {str(e)}")
            
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
            
            # Add phone and email validation to Experian API results
            try:
                logger.info("Adding phone validation to Experian API results...")
                phone_validation_result = await phone_validation_service.validate_phone_numbers(search_request)
                if phone_validation_result and phone_validation_result.get('phone_validation'):
                    result['phone_validation'] = phone_validation_result['phone_validation']
                    logger.info("Phone validation added to Experian API results")
            except Exception as e:
                logger.warning(f"Phone validation failed for Experian API results: {str(e)}")
            
            try:
                logger.info("Adding email validation to Experian API results...")
                email_validation_result = await email_validation_service.validate_email_address(search_request)
                if email_validation_result and email_validation_result.get('email_validation'):
                    result['email_validation'] = email_validation_result['email_validation']
                    logger.info("Email validation added to Experian API results")
            except Exception as e:
                logger.warning(f"Email validation failed for Experian API results: {str(e)}")
        
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
            "validate-phone": "/validate-phone",
            "health": "/health"
        }
    }
    log_api_response(logger, "/", 200, len(json.dumps(response)))
    return response

@router.post("/validate-phone")
async def validate_phone_numbers(
    search_request: SearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Validate and enrich phone numbers for contact validation
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Authenticated phone validation request from user ID: {user_id}")
    
    # Log incoming request
    log_api_request(logger, "/validate-phone", search_request.dict())
    
    try:
        # Call phone validation service
        result = await phone_validation_service.validate_phone_numbers(search_request)
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        log_api_response(logger, "/validate-phone", 200, len(response_json))
        logger.info(f"Phone validation completed successfully in {total_time:.2f} seconds")
        
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions without additional logging (already logged in service)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in phone validation endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Phone validation failed: {str(e)}"
        )

@router.post("/validate-email")
async def validate_email_address(
    search_request: SearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Validate and enrich email addresses using Experian Aperture API
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Authenticated email validation request from user ID: {user_id}")
    
    # Log incoming request
    log_api_request(logger, "/validate-email", search_request.dict())
    
    try:
        logger.info(f"Starting email validation for: {search_request.FIRST_NAME} {search_request.LAST_NAME}")
        
        # Validate email address using Experian Aperture API
        result = await email_validation_service.validate_email_address(search_request)
        
        # Log response
        total_time = time.time() - start_time
        log_api_response(logger, "/validate-email", result, total_time)
        logger.info(f"Email validation completed successfully in {total_time:.2f} seconds")
        
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions without additional logging (already logged in service)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in email validation endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Email validation failed: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    log_api_request(logger, "/health", {})
    logger.debug("Health check requested")
    response = {"status": "healthy", "service": "experian-api-integration"}
    log_api_response(logger, "/health", 200, len(json.dumps(response)))
    return response