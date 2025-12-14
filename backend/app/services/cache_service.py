"""
Cache service for managing Experian API response caching
Handles cache lookups, saves, and expiration management
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import json
import logging

from database import ExperianAPICache, generate_search_hash, get_cache_expiry_date

logger = logging.getLogger(__name__)


class CacheService:
    """Service for managing API response caching with 90-day TTL"""
    
    @staticmethod
    def find_cached_result(
        session: Session,
        first_name: str = None,
        last_name: str = None,
        address: str = None,
        city: str = None,
        state: str = None,
        zip_code: str = None
    ) -> dict | None:
        """
        Search for cached result by normalized search criteria (name + address).
        Returns complete cached response or None if not found or expired.
        
        Args:
            session: SQLAlchemy database session
            first_name, last_name, address, city, state, zip_code: Search criteria
            
        Returns:
            Dictionary with cached data or None if cache miss/expired
        """
        try:
            # Generate search hash
            search_hash = generate_search_hash(
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code
            )
            
            logger.debug(f"Searching cache for hash: {search_hash}")
            
            # Query cache by search hash
            cache_entry = session.query(ExperianAPICache).filter(
                ExperianAPICache.search_hash == search_hash
            ).first()
            
            if not cache_entry:
                logger.debug(f"Cache miss - no entry found for hash: {search_hash}")
                return None
            
            # Check if cache is expired
            if cache_entry.expires_at < datetime.utcnow():
                logger.info(f"Cache expired - hash: {search_hash}, expired at: {cache_entry.expires_at}")
                return None
            
            # Cache hit! Update access tracking
            logger.info(f"Cache hit - hash: {search_hash}, api_calls_count: {cache_entry.api_calls_count}")
            cache_entry.last_accessed_at = datetime.utcnow()
            cache_entry.api_calls_count += 1
            session.commit()
            
            # Build response from cached data (metadata tracked internally, not sent to users)
            cached_response = {
                "search_response": json.loads(cache_entry.search_response) if isinstance(cache_entry.search_response, str) else cache_entry.search_response,
                "phone_validation": json.loads(cache_entry.phone_validation) if cache_entry.phone_validation and isinstance(cache_entry.phone_validation, str) else cache_entry.phone_validation,
                "email_validation": json.loads(cache_entry.email_validation) if cache_entry.email_validation and isinstance(cache_entry.email_validation, str) else cache_entry.email_validation
            }
            
            return cached_response
            
        except Exception as e:
            logger.error(f"Error retrieving from cache: {str(e)}")
            return None
    
    @staticmethod
    def save_cache_result(
        session: Session,
        search_response: dict,
        phone_validation: dict = None,
        email_validation: dict = None,
        first_name: str = None,
        last_name: str = None,
        address: str = None,
        city: str = None,
        state: str = None,
        zip_code: str = None,
        api_source: str = "experian",
        is_partial: bool = False,
        error_message: str = None
    ) -> bool:
        """
        Save API response to cache with 90-day TTL.
        
        Args:
            session: SQLAlchemy database session
            search_response: Main search API response (all tabs)
            phone_validation: Phone validation API response (optional)
            email_validation: Email validation API response (optional)
            first_name, last_name, address, city, state, zip_code: Search criteria (name + address)
            api_source: Source identifier (default: "experian")
            is_partial: Whether only partial data was available
            error_message: Error message if API call failed
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Generate search hash
            search_hash = generate_search_hash(
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code
            )
            
            logger.debug(f"Saving cache for hash: {search_hash}")
            
            # Create cache entry
            cache_entry = ExperianAPICache(
                search_hash=search_hash,
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                search_response=json.dumps(search_response) if isinstance(search_response, dict) else search_response,
                phone_validation=json.dumps(phone_validation) if phone_validation and isinstance(phone_validation, dict) else phone_validation,
                email_validation=json.dumps(email_validation) if email_validation and isinstance(email_validation, dict) else email_validation,
                api_calls_count=1,
                expires_at=get_cache_expiry_date(),
                api_source=api_source,
                is_partial=is_partial,
                error_message=error_message
            )
            
            session.add(cache_entry)
            session.commit()
            
            logger.info(f"Successfully cached result - hash: {search_hash}, expires_at: {cache_entry.expires_at}")
            return True
            
        except IntegrityError as e:
            session.rollback()
            logger.warning(f"Cache entry already exists (likely duplicate concurrent request): {str(e)}")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving to cache: {str(e)}")
            return False
    
    @staticmethod
    def update_cache_hit_count(
        session: Session,
        search_hash: str
    ) -> bool:
        """
        Increment cache hit count for a specific cached entry.
        
        Args:
            session: SQLAlchemy database session
            search_hash: SHA256 hash of search criteria
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            cache_entry = session.query(ExperianAPICache).filter(
                ExperianAPICache.search_hash == search_hash
            ).first()
            
            if not cache_entry:
                logger.warning(f"Cache entry not found for hash: {search_hash}")
                return False
            
            cache_entry.api_calls_count += 1
            cache_entry.last_accessed_at = datetime.utcnow()
            session.commit()
            
            logger.debug(f"Updated cache hit count - hash: {search_hash}, new count: {cache_entry.api_calls_count}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating cache hit count: {str(e)}")
            return False
    
    @staticmethod
    def is_cache_expired(cache_entry: ExperianAPICache) -> bool:
        """
        Check if a cache entry has expired.
        
        Args:
            cache_entry: ExperianAPICache model instance
            
        Returns:
            True if expired, False otherwise
        """
        return cache_entry.expires_at < datetime.utcnow()
    
    @staticmethod
    def cleanup_expired_cache(session: Session, dry_run: bool = False) -> int:
        """
        Delete all expired cache entries (older than 90 days).
        
        Args:
            session: SQLAlchemy database session
            dry_run: If True, only count expired entries without deleting
            
        Returns:
            Number of entries deleted (or would be deleted if dry_run=True)
        """
        try:
            now = datetime.utcnow()
            
            # Find expired entries
            expired_entries = session.query(ExperianAPICache).filter(
                ExperianAPICache.expires_at < now
            ).all()
            
            count = len(expired_entries)
            
            if dry_run:
                logger.info(f"[DRY RUN] Would delete {count} expired cache entries")
                return count
            
            if count > 0:
                # Delete expired entries
                for entry in expired_entries:
                    session.delete(entry)
                session.commit()
                logger.info(f"Successfully deleted {count} expired cache entries")
            else:
                logger.debug("No expired cache entries found")
            
            return count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error cleaning up expired cache: {str(e)}")
            return 0
    
    @staticmethod
    def get_cache_statistics(session: Session) -> dict:
        """
        Get cache statistics for monitoring and analytics.
        
        Args:
            session: SQLAlchemy database session
            
        Returns:
            Dictionary with cache statistics
        """
        try:
            total_entries = session.query(ExperianAPICache).count()
            
            now = datetime.utcnow()
            expired_entries = session.query(ExperianAPICache).filter(
                ExperianAPICache.expires_at < now
            ).count()
            
            active_entries = total_entries - expired_entries
            
            # Calculate total cache hits
            total_hits = session.query(ExperianAPICache).with_entities(
                __import__('sqlalchemy').func.sum(ExperianAPICache.api_calls_count)
            ).scalar() or 0
            
            # Get oldest and newest cache entries
            oldest = session.query(ExperianAPICache).order_by(
                ExperianAPICache.created_at.asc()
            ).first()
            
            newest = session.query(ExperianAPICache).order_by(
                ExperianAPICache.created_at.desc()
            ).first()
            
            stats = {
                "total_entries": total_entries,
                "active_entries": active_entries,
                "expired_entries": expired_entries,
                "total_cache_hits": total_hits,
                "oldest_entry": oldest.created_at.isoformat() if oldest else None,
                "newest_entry": newest.created_at.isoformat() if newest else None,
                "cache_size_estimate_mb": "N/A"  # Would need to query actual size
            }
            
            logger.debug(f"Cache statistics: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache statistics: {str(e)}")
            return {}
