"""
Cache service for managing DataIris API response caching
Handles cache lookups, saves, and expiration management
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging
import hashlib

from database import DataIrisCache, get_cache_expiry_date

logger = logging.getLogger(__name__)


class DataIrisCacheService:
    """Service for managing DataIris API response caching with 90-day TTL"""
    
    @staticmethod
    def generate_search_hash(first_name: str = None, last_name: str = None, zip_code: str = None) -> str:
        """
        Generate a deterministic SHA256 hash from normalized search criteria (first_name + last_name + zip_code).
        Normalizes input to handle different cases/spacing and create consistent lookups.
        """
        # Normalize inputs - strip whitespace and convert to lowercase
        normalized = {
            'first_name': (first_name or '').strip().lower(),
            'last_name': (last_name or '').strip().lower(),
            'zip_code': (zip_code or '').strip().lower(),
        }
        
        # Create a consistent JSON string for hashing
        hash_input = json.dumps(normalized, sort_keys=True)
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    @staticmethod
    def find_cached_result(
        session: Session,
        first_name: str = None,
        last_name: str = None,
        zip_code: str = None
    ) -> dict | None:
        """
        Search for cached result by normalized search criteria (first_name + last_name + zip_code).
        Returns complete cached response or None if not found or expired.
        
        Args:
            session: SQLAlchemy database session
            first_name, last_name, zip_code: Search criteria
            
        Returns:
            Dictionary with cached data or None if cache miss/expired
        """
        try:
            # Generate search hash
            search_hash = DataIrisCacheService.generate_search_hash(
                first_name=first_name,
                last_name=last_name,
                zip_code=zip_code
            )
            
            logger.debug(f"Searching DataIris cache for hash: {search_hash}")
            
            # Query cache by search hash
            cache_entry = session.query(DataIrisCache).filter(
                DataIrisCache.search_hash == search_hash
            ).first()
            
            if not cache_entry:
                logger.debug(f"DataIris cache miss - no entry found for hash: {search_hash}")
                return None
            
            # Check if cache is expired
            if cache_entry.expires_at < datetime.utcnow():
                logger.info(f"DataIris cache expired - hash: {search_hash}, expired at: {cache_entry.expires_at}")
                return None
            
            # Cache hit! Update access tracking
            logger.info(f"DataIris cache hit - hash: {search_hash}, api_calls_count: {cache_entry.api_calls_count}, record_count: {cache_entry.record_count}")
            cache_entry.last_accessed_at = datetime.utcnow()
            cache_entry.api_calls_count += 1
            session.commit()
            
            # Build response from cached data
            cached_response = {
                "search_response": json.loads(cache_entry.search_response) if isinstance(cache_entry.search_response, str) else cache_entry.search_response,
                "transformed_results": json.loads(cache_entry.transformed_results) if cache_entry.transformed_results and isinstance(cache_entry.transformed_results, str) else cache_entry.transformed_results
            }
            
            return cached_response
            
        except Exception as e:
            logger.error(f"Error retrieving DataIris from cache: {str(e)}")
            return None
    
    @staticmethod
    def save_cache_result(
        session: Session,
        search_response: dict,
        transformed_results: dict = None,
        first_name: str = None,
        last_name: str = None,
        zip_code: str = None,
        record_count: int = None,
        api_source: str = "datairis",
        is_partial: bool = False,
        error_message: str = None
    ) -> bool:
        """
        Save API response to cache with 90-day TTL.
        
        Args:
            session: SQLAlchemy database session
            search_response: Main search API response
            transformed_results: Transformed results organized by category/subcategory (optional)
            first_name, last_name, zip_code: Search criteria
            record_count: Number of records returned
            api_source: Source identifier (default: "datairis")
            is_partial: Whether only partial data was available
            error_message: Error message if API call failed
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Generate search hash
            search_hash = DataIrisCacheService.generate_search_hash(
                first_name=first_name,
                last_name=last_name,
                zip_code=zip_code
            )
            
            logger.debug(f"Saving DataIris cache for hash: {search_hash}")
            
            # Create cache entry
            cache_entry = DataIrisCache(
                search_hash=search_hash,
                first_name=first_name,
                last_name=last_name,
                zip_code=zip_code,
                search_response=json.dumps(search_response) if isinstance(search_response, dict) else search_response,
                transformed_results=json.dumps(transformed_results) if transformed_results and isinstance(transformed_results, dict) else transformed_results,
                api_calls_count=1,
                expires_at=get_cache_expiry_date(),
                api_source=api_source,
                record_count=record_count,
                is_partial=is_partial,
                error_message=error_message
            )
            
            session.add(cache_entry)
            session.commit()
            
            logger.info(f"Successfully cached DataIris result - hash: {search_hash}, expires_at: {cache_entry.expires_at}, record_count: {record_count}")
            return True
            
        except IntegrityError as e:
            session.rollback()
            logger.warning(f"DataIris cache entry already exists (likely duplicate concurrent request): {str(e)}")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving DataIris to cache: {str(e)}")
            return False
