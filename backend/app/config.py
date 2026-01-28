"""
Configuration settings for the Experian API integration
"""

import os
from dotenv import load_dotenv

# Load environment variables from the backend directory (parent of app)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

# Experian API Configuration
EXPERIAN_API_URL = os.getenv("EXPERIAN_API_URL")
EXPERIAN_AUTH_TOKEN = os.getenv("EXPERIAN_AUTH_TOKEN")

# BrightData API Configuration
BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY")
BRIGHTDATA_API_URL = os.getenv("BRIGHTDATA_API_URL")

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
]

# Add origins from environment variable
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    additional_origins = env_origins.split(",")
    ALLOWED_ORIGINS.extend([origin.strip() for origin in additional_origins])

# AI Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")

# Debug environment loading
if DEBUG:
    print(f"Environment file path: {env_path}")
    print(f"Environment file exists: {os.path.exists(env_path)}")
    print(f"OPENROUTER_API_KEY loaded: {'Yes' if OPENROUTER_API_KEY else 'No'}")
    if OPENROUTER_API_KEY:
        print(f"API Key preview: {OPENROUTER_API_KEY[:10]}...")

# Configuration loaded - debug prints removed in favor of proper logging system