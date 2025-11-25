"""
Email Validation Service using Experian Aperture API

This service validates and enriches email addresses for given person information
using the Experian Aperture Identity Append API.
"""

import json
import httpx
from typing import Dict, Any
from fastapi import HTTPException
import os

from models import SearchRequest
from core.logging_config import setup_logging, log_error
from config import DEBUG, EXPERIAN_APERTURE_API_URL, EXPERIAN_APERTURE_AUTH_TOKEN


class EmailValidationService:
    """Service for validating and enriching email addresses using Experian Aperture API"""
    
    def __init__(self):
        self.logger = setup_logging(DEBUG)
        self.api_url = EXPERIAN_APERTURE_API_URL
        self.auth_token = EXPERIAN_APERTURE_AUTH_TOKEN
        self.timeout = httpx.Timeout(30.0)  # 30 second timeout
        
        if not self.auth_token:
            self.logger.error("EXPERIAN_APERTURE_AUTH_TOKEN environment variable not set")
            raise ValueError("Experian Aperture Auth Token not configured")
    
    def _build_payload(self, search_request: SearchRequest) -> Dict[str, Any]:
        """
        Build the API payload for email validation request
        
        Args:
            search_request: The search parameters containing name and address
            
        Returns:
            Formatted payload for Experian Aperture API
        """
        # Extract name components
        first_name = search_request.FIRST_NAME or ""
        middle_name = ""  # SearchRequest doesn't have middle name field
        last_name = search_request.LAST_NAME or ""
        
        # Extract address components and combine street addresses
        street1 = search_request.STREET1 or ""
        street2 = search_request.STREET2 or ""
        
        # Combine street addresses for more complete address matching
        if street1 and street2:
            address_line_1 = f"{street1}, {street2}"
        elif street1:
            address_line_1 = street1
        elif street2:
            address_line_1 = street2
        else:
            address_line_1 = ""
            
        city = search_request.CITY or ""
        state = search_request.STATE or ""
        zip_code = search_request.ZIP or ""
        
        payload = {
            "components": {
                "first_name": [first_name] if first_name else [""],
                "middle_name": [middle_name] if middle_name else [""],
                "last_name": [last_name] if last_name else [""],
                "address_line_1": [address_line_1] if address_line_1 else [""],
                "town": [city] if city else [""],
                "sub_region": [""],  # County - not typically provided in search
                "region": [state] if state else [""],
                "postal_code": [zip_code] if zip_code else [""]
            },
            "options": [],
            "attributes": ["email"]
        }
        
        return payload
    
    def _format_email_validation_response(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the email validation response for frontend consumption
        
        Args:
            api_response: Raw response from Experian Aperture API
            
        Returns:
            Formatted response with organized email data
        """
        formatted_response = {
            "email_validation": {
                "emails_found": [],
                "total_emails": 0,
                "validation_metadata": {}
            }
        }
        
        # Extract email data from result and metadata
        emails_with_details = []
        
        if "result" in api_response and "email" in api_response["result"]:
            email_address = api_response["result"]["email"]
            
            if email_address:
                # Get email type from metadata if available
                email_type = "unknown"
                if "metadata" in api_response and "email_detail" in api_response["metadata"]:
                    email_detail = api_response["metadata"]["email_detail"]
                    if isinstance(email_detail, dict):
                        email_type = email_detail.get("email_type", "unknown")
                    elif isinstance(email_detail, list) and len(email_detail) > 0:
                        email_type = email_detail[0].get("email_type", "unknown")
                
                # Create email info object
                email_info = {
                    "address": email_address,
                    "type": email_type,
                    "rank": 1
                }
                emails_with_details.append(email_info)
        
        formatted_response["email_validation"]["emails_found"] = emails_with_details
        formatted_response["email_validation"]["total_emails"] = len(emails_with_details)

        # Add summary metadata
        if formatted_response["email_validation"]["total_emails"] > 0:
            formatted_response["email_validation"]["validation_metadata"] = {
                "api_source": "experian_aperture",
                "validation_status": "success"
            }
        else:
            # No email found
            formatted_response["email_validation"]["validation_metadata"] = {
                "api_source": "experian_aperture", 
                "validation_status": "no_email_found"
            }

        return formatted_response
    
    async def validate_email_address(self, search_request: SearchRequest) -> Dict[str, Any]:
        """
        Validate and enrich email address for a given person
        
        Args:
            search_request: The search parameters containing name and address
            
        Returns:
            Formatted email validation results
            
        Raises:
            HTTPException: If API call fails or returns error
        """
        try:
            # Build the API payload
            payload = self._build_payload(search_request)
            
            # Prepare headers
            headers = {
                "Auth-Token": self.auth_token,
                "Add-Metadata": "true",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Make API call
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    # Log response details for debugging
                    try:
                        error_response = response.json()
                        error_detail = error_response.get('message', f'API returned status {response.status_code}')
                    except:
                        error_detail = response.text or f'API returned status {response.status_code}'
                    
                    error_msg = f"Email validation API failed with status {response.status_code}: {error_detail}"
                    self.logger.error(error_msg)
                    raise HTTPException(status_code=response.status_code, detail=error_msg)
                
                # Parse response
                try:
                    api_response = response.json()
                except json.JSONDecodeError as e:
                    error_msg = f"Failed to parse email validation API response: {str(e)}"
                    log_error(self.logger, error_msg, e)
                    raise HTTPException(status_code=500, detail=error_msg)
                
                # Format and return response
                formatted_response = self._format_email_validation_response(api_response)
                
                return formatted_response
                
        except HTTPException as he:
            # For now, return a structured error response instead of raising the exception
            # This allows the Contact Validation tab to still display something useful
            error_msg = f"Email validation API unavailable: {he.detail}"
            self.logger.warning(error_msg)
            
            return {
                "email_validation": {
                    "email_found": None,
                    "email_type": None,
                    "total_emails": 0,
                    "validation_metadata": {
                        "error": error_msg,
                        "api_source": "experian_aperture",
                        "validation_status": "failed"
                    }
                }
            }
        except Exception as e:
            error_msg = f"Email validation failed: {str(e)}"
            log_error(self.logger, error_msg, e)
            
            return {
                "email_validation": {
                    "email_found": None,
                    "email_type": None,
                    "total_emails": 0,
                    "validation_metadata": {
                        "error": error_msg,
                        "api_source": "experian_aperture",
                        "validation_status": "error"
                    }
                }
            }