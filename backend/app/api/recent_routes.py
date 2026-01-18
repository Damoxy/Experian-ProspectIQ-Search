"""
Recent Searches API Routes
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import time

from database import get_experian_db
from auth import get_current_user_id
from services.search_history_service import SearchHistoryService
from core.logging_config import setup_logging, log_api_request, log_api_response
from config import DEBUG

logger = setup_logging(DEBUG)
router = APIRouter(prefix="/recent", tags=["recent-searches"])
security = HTTPBearer()


class DeleteSearchRequest(BaseModel):
    """Request model for deleting searches"""
    search_ids: List[int]


@router.get("/searches")
async def get_recent_searches(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_experian_db)
):
    """
    Get user's recent searches (last 10)
    (Protected endpoint - requires authentication)
    """
    start_time = time.time()
    
    try:
        # Validate authentication token
        user_id = get_current_user_id(credentials.credentials)
        logger.info(f"Recent searches request from user ID: {user_id}")
        
        # Log incoming request
        log_api_request(logger, "/recent/searches", {"user_id": user_id})
        
        # Get recent searches
        searches = SearchHistoryService.get_recent_searches(db, user_id)
        
        # Log response and timing
        total_time = time.time() - start_time
        log_api_response(logger, "/recent/searches", 200, len(str(searches)))
        logger.info(f"Recent searches retrieved successfully in {total_time:.2f} seconds")
        
        return {
            "status": "success",
            "count": len(searches),
            "searches": searches
        }
        
    except Exception as e:
        logger.error(f"Error retrieving recent searches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recent searches"
        )


@router.delete("/searches/clear")
async def clear_recent_searches(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_experian_db)
):
    """
    Clear all recent searches for the current user
    (Protected endpoint - requires authentication)
    """
    try:
        # Validate authentication token
        user_id = get_current_user_id(credentials.credentials)
        logger.info(f"Clear searches request from user ID: {user_id}")
        
        # Log incoming request
        log_api_request(logger, "/recent/searches/clear", {"user_id": user_id})
        
        # Clear search history
        SearchHistoryService.clear_search_history(db, user_id)
        
        logger.info(f"Search history cleared for user ID: {user_id}")
        
        return {
            "status": "success",
            "message": "All recent searches cleared"
        }
        
    except Exception as e:
        logger.error(f"Error clearing search history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear search history"
        )


@router.delete("/searches/delete")
async def delete_selected_searches(
    delete_request: DeleteSearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_experian_db)
):
    """
    Delete selected searches by their IDs
    (Protected endpoint - requires authentication)
    """
    try:
        # Validate authentication token
        user_id = get_current_user_id(credentials.credentials)
        logger.info(f"Delete searches request from user ID: {user_id}, Search IDs: {delete_request.search_ids}")
        
        # Log incoming request
        log_api_request(logger, "/recent/searches/delete", {
            "user_id": user_id,
            "search_ids": delete_request.search_ids
        })
        
        # Validate that search_ids is not empty
        if not delete_request.search_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No search IDs provided"
            )
        
        # Delete selected searches
        deleted_count = SearchHistoryService.delete_multiple_searches(
            db, user_id, delete_request.search_ids
        )
        
        logger.info(f"Deleted {deleted_count} searches for user ID: {user_id}")
        
        return {
            "status": "success",
            "message": f"Successfully deleted {deleted_count} search(es)",
            "deleted_count": deleted_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting selected searches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete selected searches"
        )
