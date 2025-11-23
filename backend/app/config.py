"""
Configuration settings for the Experian API integration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Experian API Configuration
EXPERIAN_API_URL = os.getenv("EXPERIAN_API_URL")
EXPERIAN_AUTH_TOKEN = os.getenv("EXPERIAN_AUTH_TOKEN")

# Experian Aperture API Configuration (for phone validation)
EXPERIAN_APERTURE_API_URL = os.getenv("EXPERIAN_APERTURE_API_URL", "https://api.experianaperture.io/identity/append/v1")
EXPERIAN_APERTURE_AUTH_TOKEN = os.getenv("EXPERIAN_APERTURE_AUTH_TOKEN")

# Server Configuration
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://mango-meadow-088b06e1e.3.azurestaticapps.net",
]

# Add additional origins from environment variable
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    additional_origins = env_origins.split(",")
    ALLOWED_ORIGINS.extend([origin.strip() for origin in additional_origins])

# Configuration loaded - debug prints removed in favor of proper logging system