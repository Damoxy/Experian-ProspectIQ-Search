"""
Main FastAPI application with clean separation of concerns
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ALLOWED_ORIGINS, HOST, PORT, DEBUG
from api.routes import router
from api.auth_routes import router as auth_router
from api.recent_routes import router as recent_router
from api.datairis_routes import router as datairis_router
from core.logging_config import setup_logging
from services.cache_cleanup import start_cache_cleanup_scheduler, stop_cache_cleanup_scheduler

# Initialize logging
logger = setup_logging(DEBUG)


def create_app() -> FastAPI:
    """Factory function to create FastAPI application"""
    app = FastAPI(
        title="KC Experian API Integration",
        description="FastAPI backend for Experian contact and address search",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router)
    app.include_router(auth_router)
    app.include_router(recent_router)
    app.include_router(datairis_router)
    
    # Register startup event - start cache cleanup scheduler
    @app.on_event("startup")
    async def startup_event():
        logger.info("Application startup event triggered")
        logger.info("FastAPI application starting up")
        logger.info(f"Debug mode: {DEBUG}")
        logger.info(f"Server will run on {HOST}:{PORT}")
        logger.info(f"CORS origins: {ALLOWED_ORIGINS}")
        
        # Debug environment variables for AI service
        from config import OPENROUTER_API_KEY, OPENROUTER_MODEL
        if OPENROUTER_API_KEY:
            key_preview = f"{OPENROUTER_API_KEY[:10]}..." if len(OPENROUTER_API_KEY) > 10 else "KEY_TOO_SHORT"
            logger.info(f"OpenRouter API key status: Available ({key_preview})")
            logger.info(f"OpenRouter model: {OPENROUTER_MODEL}")
        else:
            logger.error("OpenRouter API key not found in environment variables")
        
        # Start cache cleanup scheduler
        try:
            start_cache_cleanup_scheduler()
        except Exception as e:
            logger.error(f"Failed to start cache cleanup scheduler: {str(e)}")
    
    # Register shutdown event - stop cache cleanup scheduler
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Application shutdown event triggered")
        try:
            stop_cache_cleanup_scheduler()
        except Exception as e:
            logger.error(f"Error during cache cleanup scheduler shutdown: {str(e)}")
    
    # Log application startup
    logger.info("FastAPI application created successfully")
    
    # Debug environment variables for AI service
    from config import OPENROUTER_API_KEY, OPENROUTER_MODEL
    if OPENROUTER_API_KEY:
        key_preview = f"{OPENROUTER_API_KEY[:10]}..." if len(OPENROUTER_API_KEY) > 10 else "KEY_TOO_SHORT"
        logger.info(f"OpenRouter API key status: Available ({key_preview})")
        logger.info(f"OpenRouter model: {OPENROUTER_MODEL}")
    else:
        logger.error("OpenRouter API key not found in environment variables")
    
    return app


# Create app instance
app = create_app()





if __name__ == "__main__":
    logger.info(f"Starting server on {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )