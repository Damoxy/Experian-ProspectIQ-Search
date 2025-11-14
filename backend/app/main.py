from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

# Import our modules
try:
    from .config import EXPERIAN_API_URL, EXPERIAN_AUTH_TOKEN, ALLOWED_ORIGINS, HOST, PORT, DEBUG
    from .models import SearchRequest
    from .utils import transform_to_experian_format
    from .data_processing import clean_response_data
    from .field_mappings import map_field_names
except ImportError:
    # Handle case when running directly
    from config import EXPERIAN_API_URL, EXPERIAN_AUTH_TOKEN, ALLOWED_ORIGINS, HOST, PORT, DEBUG
    from models import SearchRequest
    from utils import transform_to_experian_format
    from data_processing import clean_response_data
    from field_mappings import map_field_names

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





@app.post("/search")
async def search_experian(search_request: SearchRequest):
    """
    Search Experian database for contact and address information
    """
    try:
        # Transform input to Experian format
        experian_payload = transform_to_experian_format(search_request)
        
        # Prepare headers for Experian API
        headers = {
            "Auth-Token": EXPERIAN_AUTH_TOKEN,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Make request to Experian API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                EXPERIAN_API_URL,
                json=experian_payload.dict(),
                headers=headers
            )
            
            # Check if request was successful
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Experian API error: {response.text}"
                )
            
            # Parse response
            experian_data = response.json()
            
            # Clean the response data
            cleaned_data = clean_response_data(experian_data)
            
            if not cleaned_data:
                return {"message": "No data found for the provided search criteria"}
            
            # Map field names to user-friendly names
            mapped_data = map_field_names(cleaned_data)
            
            return mapped_data
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="Request to Experian API timed out"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error connecting to Experian API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "KC Experian API Integration",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "experian-api-integration"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )