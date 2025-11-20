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
from core.logging_config import setup_logging
from database import create_tables

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
    
    # Initialize database tables
    create_tables()
    
    # Log application startup
    logger.info("FastAPI application starting up")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"Server will run on {HOST}:{PORT}")
    logger.info(f"CORS origins: {ALLOWED_ORIGINS}")
    
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