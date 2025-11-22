"""
Experian API service layer - handles all business logic for Experian interactions
"""

import httpx
import time
import json
import logging
from typing import Dict, Any
from fastapi import HTTPException

from config import EXPERIAN_API_URL, EXPERIAN_AUTH_TOKEN, DEBUG
from models import SearchRequest
from utils import transform_to_experian_format
from data_processing import clean_response_data
from field_mappings import transform_experian_response
from core.logging_config import setup_logging, log_experian_request, log_experian_response, log_data_processing, log_error


class ExperianService:
    """Service class for handling Experian API operations with comprehensive logging"""
    
    def __init__(self):
        self.api_url = EXPERIAN_API_URL
        self.auth_token = EXPERIAN_AUTH_TOKEN
        self.timeout = 30.0
        self.logger = setup_logging(DEBUG)
    
    async def search(self, search_request: SearchRequest) -> Dict[str, Any]:
        """
        Perform search operation against Experian API
        
        Args:
            search_request: The search parameters
            
        Returns:
            Transformed and cleaned search results
            
        Raises:
            HTTPException: If API call fails or returns error
        """
        try:
            # Transform input to Experian format
            self.logger.debug("Transforming input to Experian format")
            experian_payload = transform_to_experian_format(search_request)
            
            # Make API call
            raw_response = await self._call_experian_api(experian_payload)
            
            # Process response
            processed_data = self._process_response(raw_response)
            
            return processed_data
            
        except httpx.TimeoutException as e:
            log_error(self.logger, e, "Experian API timeout")
            raise HTTPException(
                status_code=408,
                detail="Request to Experian API timed out"
            )
        except httpx.RequestError as e:
            log_error(self.logger, e, "Experian API connection error")
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to Experian API: {str(e)}"
            )
        except HTTPException:
            # Re-raise HTTP exceptions without additional logging
            raise
        except Exception as e:
            log_error(self.logger, e, "Search operation")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
    
    async def _call_experian_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make the actual HTTP call to Experian API with comprehensive logging"""
        headers = {
            "Auth-Token": self.auth_token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Log Experian request
        payload_json = payload.dict() if hasattr(payload, 'dict') else payload
        payload_size = len(json.dumps(payload_json))
        log_experian_request(self.logger, payload_size)
        
        # Make request to Experian API
        self.logger.info("Making request to Experian API")
        experian_start = time.time()
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.api_url,
                json=payload_json,
                headers=headers
            )
            
            # Log Experian response
            experian_time = time.time() - experian_start
            response_size = len(response.content)
            log_experian_response(self.logger, response.status_code, response_size, experian_time)
            
            if response.status_code != 200:
                self.logger.error(f"Experian API returned status {response.status_code}: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Experian API error: {response.text}"
                )
            
            return response.json()
    
    def _process_response(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and transform the raw Experian response with comprehensive logging"""
        # Parse response
        self.logger.debug("Parsing Experian API response")
        
        # Clean the response data
        raw_count = len(raw_data) if isinstance(raw_data, (list, dict)) else 1
        cleaned_data = clean_response_data(raw_data)
        cleaned_count = len(cleaned_data) if isinstance(cleaned_data, (list, dict)) else 1
        log_data_processing(self.logger, "cleaning", raw_count, cleaned_count)
        
        if not cleaned_data:
            self.logger.info("No data found for search criteria")
            return {"message": "No data found for the provided search criteria"}
        
        # Transform field names and values to user-friendly format
        self.logger.debug("Transforming response fields and values")
        transformed_data = transform_experian_response(cleaned_data)
        final_count = len(transformed_data) if isinstance(transformed_data, (list, dict)) else 1
        log_data_processing(self.logger, "transformation", cleaned_count, final_count)
        
        # Log response structure
        self._log_response_structure(transformed_data)
        
        return transformed_data
    
    def _log_response_structure(self, data: Any) -> None:
        """Log the response structure for debugging with proper logging"""
        self.logger.debug(f"Response structure type: {type(data)}")
        if isinstance(data, dict):
            self.logger.debug(f"Final response contains {len(data)} fields")
            if self.logger.isEnabledFor(logging.DEBUG):
                field_sample = list(data.keys())[:10]  # First 10 fields
                self.logger.debug(f"Sample fields: {field_sample}")
        elif isinstance(data, list) and len(data) > 0:
            self.logger.debug(f"Final response contains {len(data)} records")
            if isinstance(data[0], dict):
                self.logger.debug(f"Each record has {len(data[0])} fields")