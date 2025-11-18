"""
Application settings and configuration
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings configuration"""
    
    # Experian API Configuration
    EXPERIAN_API_URL: str = os.getenv("EXPERIAN_API_URL", "")
    EXPERIAN_AUTH_TOKEN: str = os.getenv("EXPERIAN_AUTH_TOKEN", "")
    
    # Server Configuration  
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # API Configuration
    API_TIMEOUT: float = 30.0
    MAX_RETRIES: int = 3
    
    def __init__(self):
        self._setup_additional_origins()
        if self.DEBUG:
            self._log_configuration()
    
    def _setup_additional_origins(self) -> None:
        """Add additional CORS origins from environment variable"""
        env_origins = os.getenv("ALLOWED_ORIGINS")
        if env_origins:
            additional_origins = [origin.strip() for origin in env_origins.split(",")]
            self.ALLOWED_ORIGINS.extend(additional_origins)
    
    def _log_configuration(self) -> None:
        """Log configuration for debugging"""
        print(f"DEBUG: EXPERIAN_API_URL = {self.EXPERIAN_API_URL}")
        print(f"DEBUG: PORT = {self.PORT}")
        print(f"DEBUG: DEBUG = {self.DEBUG}")
        print(f"DEBUG: ALLOWED_ORIGINS = {self.ALLOWED_ORIGINS}")


# Global settings instance
settings = Settings()