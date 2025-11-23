"""
Phone validation service using Experian Aperture API
Handles phone number validation and enrichment
"""

import httpx
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

from config import DEBUG, EXPERIAN_APERTURE_API_URL, EXPERIAN_APERTURE_AUTH_TOKEN
from models import SearchRequest
from core.logging_config import setup_logging, log_error


class PhoneValidationService:
    """Service class for handling phone validation through Experian Aperture API"""
    
    def __init__(self):
        self.api_url = EXPERIAN_APERTURE_API_URL
        self.auth_token = EXPERIAN_APERTURE_AUTH_TOKEN
        self.timeout = 30.0
        self.logger = setup_logging(DEBUG)
        
        if not self.auth_token:
            raise ValueError("EXPERIAN_APERTURE_AUTH_TOKEN environment variable is required")
    
    def _build_payload(self, search_request: SearchRequest) -> Dict[str, Any]:
        """
        Build the payload for phone validation API from search request
        
        Args:
            search_request: The original search parameters
            
        Returns:
            Formatted payload for Experian Aperture API
        """
        # Extract name components
        first_name = search_request.FIRST_NAME or ""
        middle_name = ""  # SearchRequest doesn't have middle name field
        last_name = search_request.LAST_NAME or ""
        
        # Extract address components
        address_line_1 = search_request.STREET1 or ""
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
            "options": [
                {
                    "name": "dnc_preference",
                    "value": "flag"
                }
            ],
            "attributes": ["phone"]
        }
        
        return payload
    
    def _format_phone_validation_response(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the phone validation response for frontend consumption
        
        Args:
            api_response: Raw response from Experian Aperture API
            
        Returns:
            Formatted response with organized phone data
        """
        formatted_response = {
            "phone_validation": {
                "phones_found": [],
                "mobile_phones": [],
                "landline_phones": [],
                "dnc_compliant_phones": [],
                "non_dnc_phones": [],
                "total_phones": 0,
                "validation_metadata": {}
            }
        }
        
        # Extract phone data from result
        if "result" in api_response and "phones" in api_response["result"]:
            phones = api_response["result"]["phones"]
            formatted_response["phone_validation"]["phones_found"] = phones
            formatted_response["phone_validation"]["total_phones"] = len(phones)
        
        # Extract detailed metadata
        if "metadata" in api_response and "phone_detail" in api_response["metadata"]:
            phone_details = api_response["metadata"]["phone_detail"]
            
            mobile_phones = []
            landline_phones = []
            dnc_compliant = []
            non_dnc = []
            
            for phone_detail in phone_details:
                phone_info = {
                    "number": phone_detail.get("number", ""),
                    "type": phone_detail.get("phone_type", ""),
                    "dnc_status": phone_detail.get("dnc", False),
                    "dnc_date": phone_detail.get("dnc_date_revised", ""),
                    "rank": phone_detail.get("rank", 0)
                }
                
                # Categorize by phone type
                if phone_detail.get("phone_type") == "mobile":
                    mobile_phones.append(phone_info)
                elif phone_detail.get("phone_type") == "landline":
                    landline_phones.append(phone_info)
                
                # Categorize by DNC status
                if phone_detail.get("dnc", False):
                    dnc_compliant.append(phone_info)
                else:
                    non_dnc.append(phone_info)
            
            # Sort by rank (priority)
            mobile_phones.sort(key=lambda x: x["rank"])
            landline_phones.sort(key=lambda x: x["rank"])
            dnc_compliant.sort(key=lambda x: x["rank"])
            non_dnc.sort(key=lambda x: x["rank"])
            
            formatted_response["phone_validation"]["mobile_phones"] = mobile_phones
            formatted_response["phone_validation"]["landline_phones"] = landline_phones
            formatted_response["phone_validation"]["dnc_compliant_phones"] = dnc_compliant
            formatted_response["phone_validation"]["non_dnc_phones"] = non_dnc
            
            # Add summary metadata
            formatted_response["phone_validation"]["validation_metadata"] = {
                "mobile_count": len(mobile_phones),
                "landline_count": len(landline_phones),
                "dnc_compliant_count": len(dnc_compliant),
                "non_dnc_count": len(non_dnc),
                "api_source": "experian_aperture",
                "validation_date": phone_details[0].get("dnc_date_revised", "") if phone_details else ""
            }
        
        return formatted_response
    
    async def validate_phone_numbers(self, search_request: SearchRequest) -> Dict[str, Any]:
        """
        Validate and enrich phone numbers for a given person
        
        Args:
            search_request: The search parameters containing name and address
            
        Returns:
            Formatted phone validation results
            
        Raises:
            HTTPException: If API call fails or returns error
        """
        try:
            self.logger.info("Starting phone validation request")
            
            # Build the API payload
            payload = self._build_payload(search_request)
            self.logger.info(f"Phone validation payload: {json.dumps(payload, indent=2)}")
            
            # Prepare headers
            headers = {
                "Auth-Token": self.auth_token,
                "Add-Metadata": "true",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Log headers (without showing the full auth token for security)
            safe_headers = {k: (v if k != "Auth-Token" else f"{v[:8]}...{v[-4:]}") for k, v in headers.items()}
            self.logger.info(f"Phone validation headers: {json.dumps(safe_headers, indent=2)}")
            
            # Make API call
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                self.logger.info(f"Phone validation API response status: {response.status_code}")
                
                if response.status_code != 200:
                    # Log response details for debugging
                    try:
                        error_response = response.json()
                        self.logger.error(f"Phone validation API error response: {json.dumps(error_response, indent=2)}")
                        error_detail = error_response.get('message', f'API returned status {response.status_code}')
                    except:
                        error_detail = response.text or f'API returned status {response.status_code}'
                        self.logger.error(f"Phone validation API error text: {error_detail}")
                    
                    error_msg = f"Phone validation API failed with status {response.status_code}: {error_detail}"
                    self.logger.error(error_msg)
                    raise HTTPException(status_code=response.status_code, detail=error_msg)
                
                # Parse response
                try:
                    api_response = response.json()
                    self.logger.debug(f"Phone validation API response: {json.dumps(api_response, indent=2)}")
                except json.JSONDecodeError as e:
                    error_msg = f"Failed to parse phone validation API response: {str(e)}"
                    log_error(self.logger, error_msg, e)
                    raise HTTPException(status_code=500, detail=error_msg)
                
                # Format and return response
                formatted_response = self._format_phone_validation_response(api_response)
                self.logger.info("Phone validation completed successfully")
                
                return formatted_response
                
        except HTTPException as he:
            # For now, return a structured error response instead of raising the exception
            # This allows the Contact Validation tab to still display something useful
            error_msg = f"Phone validation API unavailable: {he.detail}"
            self.logger.warning(error_msg)
            
            return {
                "phone_validation": {
                    "phones_found": [],
                    "mobile_phones": [],
                    "landline_phones": [],
                    "dnc_compliant_phones": [],
                    "non_dnc_phones": [],
                    "total_phones": 0,
                    "validation_metadata": {
                        "error": error_msg,
                        "api_source": "experian_aperture",
                        "validation_status": "failed"
                    }
                }
            }
        except Exception as e:
            error_msg = f"Phone validation failed: {str(e)}"
            log_error(self.logger, error_msg, e)
            
            return {
                "phone_validation": {
                    "phones_found": [],
                    "mobile_phones": [],
                    "landline_phones": [],
                    "dnc_compliant_phones": [],
                    "non_dnc_phones": [],
                    "total_phones": 0,
                    "validation_metadata": {
                        "error": error_msg,
                        "api_source": "experian_aperture",
                        "validation_status": "error"
                    }
                }
            }