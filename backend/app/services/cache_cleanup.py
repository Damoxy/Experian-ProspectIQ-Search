"""
Background scheduler for cache cleanup
Deletes expired cache entries (>90 days old) on a scheduled basis
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

from database import ExperianSessionLocal
from services.cache_service import CacheService

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def cleanup_expired_cache_job():
    """
    Background job to clean up expired cache entries.
    Runs daily at 2 AM (02:00).
    """
    try:
        logger.info("Starting scheduled cache cleanup job...")
        session = ExperianSessionLocal()
        
        try:
            # Get statistics before cleanup
            stats_before = CacheService.get_cache_statistics(session)
            logger.info(f"Cache statistics before cleanup: {stats_before}")
            
            # Perform cleanup
            deleted_count = CacheService.cleanup_expired_cache(session, dry_run=False)
            
            # Get statistics after cleanup
            stats_after = CacheService.get_cache_statistics(session)
            logger.info(f"Cache cleanup completed. Deleted {deleted_count} entries")
            logger.info(f"Cache statistics after cleanup: {stats_after}")
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error in scheduled cache cleanup job: {str(e)}")


def start_cache_cleanup_scheduler():
    """
    Start the background scheduler for cache cleanup.
    Schedules cleanup to run daily at 2:00 AM.
    """
    global scheduler
    
    try:
        if scheduler is None:
            scheduler = BackgroundScheduler()
            
            # Schedule cleanup job to run daily at 2 AM
            scheduler.add_job(
                func=cleanup_expired_cache_job,
                trigger=CronTrigger(hour=2, minute=0),
                id="cache_cleanup_job",
                name="Expired Cache Cleanup",
                replace_existing=True,
                max_instances=1  # Prevent concurrent executions
            )
            
            scheduler.start()
            logger.info("Cache cleanup scheduler started. Cleanup scheduled daily at 2:00 AM")
        else:
            logger.info("Cache cleanup scheduler already running")
            
    except Exception as e:
        logger.error(f"Error starting cache cleanup scheduler: {str(e)}")


def stop_cache_cleanup_scheduler():
    """
    Stop the background scheduler for cache cleanup.
    Should be called during application shutdown.
    """
    global scheduler
    
    try:
        if scheduler is not None and scheduler.running:
            scheduler.shutdown()
            scheduler = None
            logger.info("Cache cleanup scheduler stopped")
    except Exception as e:
        logger.error(f"Error stopping cache cleanup scheduler: {str(e)}")


def get_next_cleanup_time():
    """
    Get the next scheduled cleanup time.
    
    Returns:
        datetime object or None if scheduler not running
    """
    global scheduler
    
    try:
        if scheduler is not None and scheduler.running:
            job = scheduler.get_job("cache_cleanup_job")
            if job:
                return job.next_run_time
    except Exception as e:
        logger.error(f"Error getting next cleanup time: {str(e)}")
    
    return None


def trigger_immediate_cleanup(dry_run: bool = True):
    """
    Manually trigger an immediate cache cleanup (useful for testing/admin).
    
    Args:
        dry_run: If True, only counts entries without deleting
        
    Returns:
        Number of entries that were (or would be) deleted
    """
    try:
        logger.info(f"Triggering immediate cache cleanup (dry_run={dry_run})...")
        session = ExperianSessionLocal()
        
        try:
            deleted_count = CacheService.cleanup_expired_cache(session, dry_run=dry_run)
            logger.info(f"Immediate cleanup completed. Affected entries: {deleted_count}")
            return deleted_count
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error in immediate cache cleanup: {str(e)}")
        return 0
