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
import asyncio

from models import SearchRequest
from services.experian_service import ExperianService
from services.knowledgecore_service import KnowledgeCoreService
from services.phone_validation_service import PhoneValidationService
from services.email_validation_service import EmailValidationService
from services.ai_insights_service import AIInsightsService
from services.cache_service import CacheService
from services.search_history_service import SearchHistoryService
from services.brightdata_service import BrightDataService
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
brightdata_service = BrightDataService()
security = HTTPBearer()

@router.post("/search")
async def unified_search(
    search_request: SearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    experian_db: Session = Depends(get_experian_db),
    givingtrend_db: Session = Depends(get_givingtrend_db)
):
    """
    Unified search endpoint that aggregates data from all sources in parallel:
    - GivingTrend Database (no cache)
    - Experian API (with cache check)
    - DataIris API (with cache check)
    - Phone Validation (with cache check)
    - Email Validation (with cache check)
    
    Returns primary result with all data merged, maintaining existing response format.
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Authenticated unified search request from user ID: {user_id}")
    
    # Log incoming request
    log_api_request(logger, "/search", search_request.dict())
    
    try:
        logger.info("Starting unified search across all sources (parallel execution)...")
        
        # Define coroutines for parallel execution
        async def get_database_results():
            try:
                logger.info("Searching GivingTrend database...")
                db_results = await kc_service.search_donors(search_request, givingtrend_db)
                if db_results:
                    logger.info(f"Found {len(db_results)} records in GivingTrend database")
                    formatted = kc_service.format_consumer_behavior_response(db_results, search_request, givingtrend_db)
                    return {"status": "success", "record_count": len(db_results), "data": formatted}
                else:
                    logger.info("No records found in GivingTrend database")
                    return {"status": "success", "record_count": 0, "data": None}
            except Exception as e:
                logger.warning(f"Database search failed: {str(e)}")
                return {"status": "error", "error": str(e), "record_count": 0, "data": None}
        
        async def get_experian_results():
            try:
                logger.info("Searching Experian (checking cache first)...")
                # Check cache first
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
                    logger.info("Experian cache hit!")
                    return {"status": "success", "from_cache": True, "data": cache_result['search_response']}
                
                # Cache miss - call Experian API
                logger.info("Experian cache miss - calling API...")
                experian_result = await experian_service.search(search_request)
                
                # Cache the result
                if isinstance(experian_result, dict):
                    CacheService.save_cache_result(
                        session=experian_db,
                        search_response=experian_result,
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
                    logger.info("Experian results cached")
                
                return {"status": "success", "from_cache": False, "data": experian_result}
            except Exception as e:
                logger.warning(f"Experian search failed: {str(e)}")
                return {"status": "error", "error": str(e), "data": None}
        
        async def get_datairis_results():
            try:
                logger.info("Searching DataIris (checking cache first)...")
                datairis_service = DataIrisService(db_session=experian_db)
                
                # DataIris service handles cache internally
                result = datairis_service.search(
                    first_name=search_request.FIRST_NAME,
                    last_name=search_request.LAST_NAME,
                    zip_code=search_request.ZIP,
                    start=1,
                    end=10
                )
                
                if result:
                    logger.info("DataIris search completed")
                    # Return properly formatted DataIris response
                    raw_results = result.get("search_response")
                    organized_results = result.get("transformed_results") or {}
                    
                    record_count = 0
                    if raw_results and isinstance(raw_results, dict):
                        record_count = raw_results.get("totalCount", 0)
                    
                    logger.info(f"DataIris found {record_count} records, organized_results type: {type(organized_results)}")
                    
                    return {
                        "status": "success",
                        "record_count": record_count,
                        "data": {
                            "status": "success",
                            "record_count": record_count,
                            "results": organized_results
                        }
                    }
                else:
                    logger.info("No DataIris results found (None returned)")
                    return {
                        "status": "success",
                        "record_count": 0,
                        "data": {
                            "status": "success",
                            "record_count": 0,
                            "results": {}
                        }
                    }
            except Exception as e:
                logger.warning(f"DataIris search failed: {str(e)}")
                return {"status": "error", "error": str(e), "record_count": 0, "data": None}
        
        async def get_phone_validation():
            try:
                logger.info("Phone validation (checking cache first)...")
                # Phone validation result is already cached in experian_api_cache table
                cache_result = CacheService.find_cached_result(
                    session=experian_db,
                    first_name=search_request.FIRST_NAME,
                    last_name=search_request.LAST_NAME,
                    address=search_request.STREET1,
                    city=search_request.CITY,
                    state=search_request.STATE,
                    zip_code=search_request.ZIP
                )
                
                if cache_result and cache_result.get('phone_validation'):
                    logger.info("Phone validation cache hit")
                    return {"status": "success", "from_cache": True, "data": cache_result['phone_validation']}
                
                logger.info("Phone validation cache miss - calling service...")
                result = await phone_validation_service.validate_phone_numbers(search_request)
                
                if result and result.get('phone_validation'):
                    logger.info("Phone validation successful")
                    return {"status": "success", "from_cache": False, "data": result['phone_validation']}
                else:
                    return {"status": "success", "from_cache": False, "data": None}
            except Exception as e:
                logger.warning(f"Phone validation failed: {str(e)}")
                return {"status": "error", "error": str(e), "data": None}
        
        async def get_email_validation():
            try:
                logger.info("Email validation (checking cache first)...")
                # Email validation result is already cached in experian_api_cache table
                cache_result = CacheService.find_cached_result(
                    session=experian_db,
                    first_name=search_request.FIRST_NAME,
                    last_name=search_request.LAST_NAME,
                    address=search_request.STREET1,
                    city=search_request.CITY,
                    state=search_request.STATE,
                    zip_code=search_request.ZIP
                )
                
                if cache_result and cache_result.get('email_validation'):
                    logger.info("Email validation cache hit")
                    return {"status": "success", "from_cache": True, "data": cache_result['email_validation']}
                
                logger.info("Email validation cache miss - calling service...")
                result = await email_validation_service.validate_email_address(search_request)
                
                if result and result.get('email_validation'):
                    logger.info("Email validation successful")
                    return {"status": "success", "from_cache": False, "data": result['email_validation']}
                else:
                    return {"status": "success", "from_cache": False, "data": None}
            except Exception as e:
                logger.warning(f"Email validation failed: {str(e)}")
                return {"status": "error", "error": str(e), "data": None}
        
        # Execute all searches in parallel
        db_result, experian_result, datairis_result, phone_result, email_result = await asyncio.gather(
            get_database_results(),
            get_experian_results(),
            get_datairis_results(),
            get_phone_validation(),
            get_email_validation(),
            return_exceptions=False
        )
        
        # Determine primary result: Database first (if found), otherwise Experian
        result = None
        if db_result["status"] == "success" and db_result.get("data"):
            result = db_result["data"]
            logger.info("Using database results as primary")
        elif experian_result["status"] == "success" and experian_result.get("data"):
            result = experian_result["data"]
            logger.info("Using Experian results as primary")
        
        # If no primary result found, return empty structure
        if not result:
            result = {
                "message": "No records found",
                "results": {}
            }
        
        # Always add Experian data alongside primary result (if it's not already the primary)
        if db_result["status"] == "success" and db_result.get("data") and experian_result["status"] == "success" and experian_result.get("data"):
            result["experian"] = experian_result["data"]
            logger.info("Experian data added alongside database results")
        
        # Add DataIris data to result (always, regardless of source)
        if datairis_result["status"] == "success" and datairis_result.get("data"):
            result["datairis"] = datairis_result["data"]
            logger.info(f"DataIris data added to result. DataIris result structure: {type(datairis_result.get('data'))}")
        else:
            logger.warning(f"DataIris data not added. Status: {datairis_result.get('status')}, Has data: {bool(datairis_result.get('data'))}")
        
        # Add phone validation to result
        if phone_result["status"] == "success" and phone_result.get("data"):
            result["phone_validation"] = phone_result["data"]
            logger.info("Phone validation data added to result")
        
        # Add email validation to result
        if email_result["status"] == "success" and email_result.get("data"):
            result["email_validation"] = email_result["data"]
            logger.info("Email validation data added to result")
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        log_api_response(logger, "/search", 200, len(response_json))
        logger.info(f"Unified search completed in {total_time:.2f} seconds")
        
        # Add to search history (non-blocking)
        try:
            SearchHistoryService.add_search(experian_db, user_id, search_request)
        except Exception as e:
            logger.warning(f"Failed to add search to history: {str(e)}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in unified search endpoint: {str(e)}")
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
            Gift_Pledge_Balance,
            Campaign_ID,
            Fund_Description
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
                "gift_pledge_balance": float(row.Gift_Pledge_Balance) if row.Gift_Pledge_Balance else 0.0,
                "campaign_id": row.Campaign_ID if row.Campaign_ID else "N/A",
                "fund_description": row.Fund_Description if row.Fund_Description else "N/A"
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

@router.post("/philanthropy/contributions")
async def get_philanthropy_contributions(
    donor_name: str,
    city: str,
    state: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get donation/contribution records for a specific person from BrightData
    Query format: "Find all donations made by [donor_name] of [city, state]"
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    # Validate authentication token
    user_id = get_current_user_id(credentials.credentials)
    logger.info(f"Philanthropy query from user ID: {user_id}")
    
    # Log incoming request
    log_api_request(logger, "/philanthropy/contributions", {
        "donor_name": donor_name,
        "city": city,
        "state": state
    })
    
    try:
        # Query BrightData for donation records
        logger.info(f"Querying BrightData for donations by {donor_name} from {city}, {state}")
        result = await brightdata_service.search_donations(donor_name, city, state)
        
        # Log successful completion
        total_time = time.time() - start_time
        response_json = json.dumps(result)
        log_api_response(logger, "/philanthropy/contributions", 200, len(response_json))
        logger.info(f"Philanthropy query completed successfully in {total_time:.2f} seconds")
        
        return result
        
    except HTTPException as http_exc:
        logger.error(f"HTTP error in philanthropy query: {http_exc.detail}")
        raise
    except Exception as e:
        error_msg = f"Error querying philanthropy data: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    log_api_request(logger, "/health", {})
    logger.debug("Health check requested")
    response = {"status": "healthy", "service": "experian-api-integration"}
    log_api_response(logger, "/health", 200, len(json.dumps(response)))
    return response