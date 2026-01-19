"""
API router for Experian search endpoints with comprehensive logging
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
import time
import os

from models import SearchRequest
from services.experian_service import ExperianService
from services.knowledgecore_service import KnowledgeCoreService
from services.phone_validation_service import PhoneValidationService
from services.email_validation_service import EmailValidationService
from services.ai_insights_service import AIInsightsService
from services.cache_service import CacheService
from services.search_history_service import SearchHistoryService
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
ai_insights_service = AIInsightsService()
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
            
            # Add to search history (async, don't block response)
            try:
                SearchHistoryService.add_search(experian_db, user_id, search_request)
            except Exception as e:
                logger.warning(f"Failed to add search to history: {str(e)}")
            
            return result
        
        # Step 2: No records found in database - fall back to Experian API
        logger.info("No records found in GivingTrend database, falling back to Experian API...")
        
        # Step 2a: Check cache before calling Experian API
        logger.info("Checking cache for previous Experian API results...")
        cache_result = CacheService.find_cached_result(
            session=experian_db,
            first_name=search_request.FIRST_NAME,
            last_name=search_request.LAST_NAME,
            address=search_request.STREET1,
            city=search_request.CITY,
            state=search_request.STATE,
            zip_code=search_request.ZIP
        )
        
        if cache_result:
            # Cache hit - return cached results
            logger.info("Cache hit! Returning cached Experian API results")
            result = cache_result['search_response']
            if cache_result.get('phone_validation'):
                result['phone_validation'] = cache_result['phone_validation']
            if cache_result.get('email_validation'):
                result['email_validation'] = cache_result['email_validation']
            
            # Log successful completion
            total_time = time.time() - start_time
            response_json = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
            log_api_response(logger, "/search", 200, len(response_json))
            logger.info(f"Cache hit completed in {total_time:.2f} seconds")
            
            # Track search history
            try:
                SearchHistoryService.add_search(experian_db, user_id, search_request)
            except Exception as e:
                logger.warning(f"Failed to add search to history: {str(e)}")
            
            return result
        
        # Step 2b: Cache miss - call Experian API
        logger.info("Cache miss - calling Experian API...")
        result = await experian_service.search(search_request)
        
        # Add source indicator to show this came from Experian fallback
        if isinstance(result, dict):
            result["fallback_source"] = "experian_api"
            result["database_checked"] = True
            result["database_records_found"] = 0
            
            # Add phone and email validation to Experian API results
            phone_validation_result = None
            email_validation_result = None
            
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
            
            # Step 2c: Save results to cache
            logger.info("Saving Experian API results to cache...")
            cache_saved = CacheService.save_cache_result(
                session=experian_db,
                search_response=result,
                phone_validation=phone_validation_result.get('phone_validation') if phone_validation_result else None,
                email_validation=email_validation_result.get('email_validation') if email_validation_result else None,
                first_name=search_request.FIRST_NAME,
                last_name=search_request.LAST_NAME,
                address=search_request.STREET1,
                city=search_request.CITY,
                state=search_request.STATE,
                zip_code=search_request.ZIP,
                api_source="experian",
                is_partial=False,
                error_message=None
            )
            
            if cache_saved:
                logger.info("Successfully cached Experian API results")
            else:
                logger.warning("Failed to cache Experian API results (may be duplicate request)")
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        log_api_response(logger, "/search", 200, len(response_json))
        logger.info(f"Fallback search completed successfully in {total_time:.2f} seconds")
        
        # Track search history
        try:
            SearchHistoryService.add_search(experian_db, user_id, search_request)
        except Exception as e:
            logger.warning(f"Failed to add search to history: {str(e)}")
        
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

@router.post("/ai-insights")
async def generate_ai_insights(
    request_data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Generate AI insights for donor profile data
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"AI insights request from user ID: {user_id}")
    
    # Extract category and profile data from request
    category = request_data.get("category", "Profile")
    profile_data = request_data.get("profile_data", {})
    
    if not profile_data:
        raise HTTPException(
            status_code=400,
            detail="Profile data is required for AI insights generation"
        )
    
    # Log incoming request (without full profile data for privacy)
    log_api_request(logger, "/ai-insights", {"category": category, "has_profile_data": bool(profile_data)})
    
    try:
        logger.info(f"Generating AI insights for category: {category}")
        
        # Generate AI insights
        result = await ai_insights_service.generate_insights(category, profile_data)
        
        # Log response and timing
        total_time = time.time() - start_time
        log_api_response(logger, "/ai-insights", {"status": "success", "category": category}, total_time)
        logger.info(f"AI insights generated successfully in {total_time:.2f} seconds")
        
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions without additional logging (already logged in service)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in AI insights endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI insights generation failed: {str(e)}"
        )

@router.get("/transactions/{constituent_id}")
async def get_transactions(
    constituent_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    givingtrend_db: Session = Depends(get_givingtrend_db)
):
    """
    Get transaction history for a constituent from GivingTrend database
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Authenticated transaction request from user ID: {user_id} for constituent: {constituent_id}")
    
    # Log incoming request
    log_api_request(logger, f"/transactions/{constituent_id}", {"constituent_id": constituent_id})
    
    try:
        # Query transactions from GivingTrend database
        logger.info(f"Fetching transactions for constituent_id: {constituent_id}")
        
        # Use environment variable for database name
        gt_db_name = os.getenv("KC_GT_DB_DATABASE")
        
        query = text(f"""
        SELECT 
            Gift_Date,
            Gift_Amount,
            Gift_Type,
            Gift_Pledge_Balance
        FROM [{gt_db_name}].[dbo].[Transaction]
        WHERE Constituent_ID = :constituent_id
        ORDER BY Gift_Date DESC
        """)
        
        result = givingtrend_db.execute(query, {"constituent_id": constituent_id})
        transactions = result.fetchall()
        
        if not transactions:
            logger.info(f"No transactions found for constituent_id: {constituent_id}")
            return {
                "constituent_id": constituent_id,
                "transactions": [],
                "total_count": 0
            }
        
        # Format transactions
        formatted_transactions = []
        for row in transactions:
            # Clean gift amount the same way as calculate_gift_metrics
            try:
                amount_str = str(row.Gift_Amount).replace('$', '').replace(',', '').strip()
                gift_amount = float(amount_str) if amount_str and amount_str not in ['', 'None', 'NULL'] else 0.0
            except (ValueError, TypeError):
                gift_amount = 0.0
            
            formatted_transactions.append({
                "gift_date": row.Gift_Date.strftime("%Y-%m-%d") if row.Gift_Date else None,
                "gift_amount": gift_amount,
                "gift_type": row.Gift_Type if row.Gift_Type else "Unknown",
                "gift_pledge_balance": float(row.Gift_Pledge_Balance) if row.Gift_Pledge_Balance else 0.0
            })
        
        logger.info(f"Found {len(formatted_transactions)} transactions for constituent_id: {constituent_id}")
        
        response = {
            "constituent_id": constituent_id,
            "transactions": formatted_transactions,
            "total_count": len(formatted_transactions)
        }
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(response)
        log_api_response(logger, f"/transactions/{constituent_id}", 200, len(response_json))
        logger.info(f"Transaction fetch completed in {total_time:.2f} seconds")
        
        return response
        
    except Exception as e:
        logger.error(f"Error fetching transactions for constituent {constituent_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch transactions: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    log_api_request(logger, "/health", {})
    logger.debug("Health check requested")
    response = {"status": "healthy", "service": "experian-api-integration"}
    log_api_response(logger, "/health", 200, len(json.dumps(response)))
    return response