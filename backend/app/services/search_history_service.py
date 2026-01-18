"""
Search History Service - Manages user search history
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Dict, Any
from database import SearchHistory, User
from models import SearchRequest


class SearchHistoryService:
    """Service for managing user search history"""
    
    @staticmethod
    def add_search(
        db: Session,
        user_id: int,
        search_request: SearchRequest
    ) -> SearchHistory:
        """
        Add a new search to user's history
        Automatically removes old searches if limit exceeded (keeps last 50)
        """
        # Create new search history entry
        search_entry = SearchHistory(
            user_id=user_id,
            first_name=search_request.FIRST_NAME or "",
            last_name=search_request.LAST_NAME or "",
            street=search_request.STREET1 or "",
            city=search_request.CITY or "",
            state=search_request.STATE or "",
            zip_code=search_request.ZIP or "",
            searched_at=datetime.utcnow()
        )
        
        db.add(search_entry)
        db.commit()
        db.refresh(search_entry)
        
        # Clean up old searches - keep only last 50
        SearchHistoryService._cleanup_old_searches(db, user_id)
        
        return search_entry
    
    @staticmethod
    def _cleanup_old_searches(db: Session, user_id: int, keep_count: int = 50) -> None:
        """Remove old searches when limit exceeded"""
        # Count current searches for user
        current_count = db.query(SearchHistory).filter(
            SearchHistory.user_id == user_id
        ).count()
        
        if current_count > keep_count:
            # Find searches to delete (older than the 50th most recent)
            searches_to_keep = db.query(SearchHistory).filter(
                SearchHistory.user_id == user_id
            ).order_by(desc(SearchHistory.searched_at)).limit(keep_count).all()
            
            # Get IDs of searches to keep
            keep_ids = [s.id for s in searches_to_keep]
            
            # Delete older searches
            db.query(SearchHistory).filter(
                SearchHistory.user_id == user_id,
                ~SearchHistory.id.in_(keep_ids)
            ).delete()
            
            db.commit()
    
    @staticmethod
    def get_recent_searches(db: Session, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's recent searches (most recent first)"""
        searches = db.query(SearchHistory).filter(
            SearchHistory.user_id == user_id
        ).order_by(desc(SearchHistory.searched_at)).limit(limit).all()
        
        # Format response
        result = []
        for search in searches:
            # Build full name and address
            full_name = f"{search.first_name} {search.last_name}".strip()
            address_parts = [search.street, search.city, search.state, search.zip_code]
            full_address = ", ".join([part for part in address_parts if part]).strip()
            
            # Calculate time ago
            time_diff = datetime.utcnow() - search.searched_at
            time_ago = SearchHistoryService._format_time_ago(time_diff)
            
            result.append({
                "id": search.id,
                "name": full_name,
                "address": full_address,
                "date": time_ago,
                "first_name": search.first_name,
                "last_name": search.last_name,
                "street": search.street,
                "city": search.city,
                "state": search.state,
                "zip_code": search.zip_code,
                "searched_at": search.searched_at.isoformat()
            })
        
        return result
    
    @staticmethod
    def _format_time_ago(time_diff) -> str:
        """Format timedelta to 'X time ago' format"""
        total_seconds = int(time_diff.total_seconds())
        
        if total_seconds < 60:
            return "just now"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes}m ago"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{hours}h ago"
        elif total_seconds < 604800:
            days = total_seconds // 86400
            return f"{days}d ago"
        else:
            weeks = total_seconds // 604800
            return f"{weeks}w ago"
    
    @staticmethod
    def delete_search(db: Session, user_id: int, search_id: int) -> bool:
        """Delete a specific search by ID (verifies ownership)"""
        search = db.query(SearchHistory).filter(
            SearchHistory.id == search_id,
            SearchHistory.user_id == user_id
        ).first()
        
        if search:
            db.delete(search)
            db.commit()
            return True
        return False
    
    @staticmethod
    def delete_multiple_searches(db: Session, user_id: int, search_ids: List[int]) -> int:
        """Delete multiple searches by IDs (verifies ownership)"""
        # Delete only searches that belong to the user
        deleted_count = db.query(SearchHistory).filter(
            SearchHistory.id.in_(search_ids),
            SearchHistory.user_id == user_id
        ).delete()
        
        db.commit()
        return deleted_count
    
    @staticmethod
    def clear_search_history(db: Session, user_id: int) -> None:
        """Clear all search history for a user"""
        db.query(SearchHistory).filter(
            SearchHistory.user_id == user_id
        ).delete()
        db.commit()
