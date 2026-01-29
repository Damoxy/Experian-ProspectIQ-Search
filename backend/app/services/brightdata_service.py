"""
BrightData API service layer - handles all business logic for BrightData interactions
for querying donation/philanthropy data
"""

import httpx
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

from config import BRIGHTDATA_API_KEY, BRIGHTDATA_API_URL, DEBUG
from core.logging_config import setup_logging


class BrightDataService:
    """Service class for handling BrightData API operations"""
    
    def __init__(self):
        self.api_key = BRIGHTDATA_API_KEY
        self.base_url = BRIGHTDATA_API_URL
        self.timeout = 60.0
        self.logger = setup_logging(DEBUG)
    
    def _get_headers(self) -> Dict[str, str]:
        """Generate headers for BrightData API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def search_donations(self, donor_name: str, city: str, state: str) -> Dict[str, Any]:
        """
        Search for donations made by a specific person
        
        Args:
            donor_name: Full name of the donor
            city: City where donor resides
            state: State where donor resides
            
        Returns:
            Dictionary containing donation records with structured data
            
        Raises:
            HTTPException: If API call fails
        """
        
        if not self.api_key:
            self.logger.error("BrightData API key not configured")
            raise HTTPException(
                status_code=500,
                detail="BrightData API key not configured"
            )
        
        try:
            # Format query as specified
            query = f'Find all donations given by "{donor_name}"'
            
            self.logger.info(f"Querying BrightData for donations: {query}")
            
            payload = {
                "query": query
            }
            
            headers = self._get_headers()
            
            # Step 1: Make request to create a preview
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/preview",
                    json=payload,
                    headers=headers
                )
            
            self.logger.info(f"BrightData preview creation status: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = f"BrightData API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to create donation preview in BrightData"
                )
            
            preview_response = response.json()
            self.logger.debug(f"BrightData preview response: {json.dumps(preview_response, indent=2)}")
            
            preview_id = preview_response.get("preview_id")
            if not preview_id:
                error_msg = "No preview_id returned from BrightData"
                self.logger.error(error_msg)
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create donation preview"
                )
            
            self.logger.info(f"Preview created with ID: {preview_id}")
            
            # Step 2: Fetch the actual data using the preview_id
            self.logger.info(f"Fetching data for preview: {preview_id}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                data_response = await client.get(
                    f"{self.base_url}/preview/{preview_id}",
                    headers=headers
                )
            
            self.logger.info(f"BrightData data fetch status: {data_response.status_code}")
            
            if data_response.status_code != 200:
                error_msg = f"BrightData data fetch error: {data_response.status_code}"
                self.logger.error(error_msg)
                raise HTTPException(
                    status_code=data_response.status_code,
                    detail="Failed to retrieve donation data"
                )
            
            response_data = data_response.json()
            self.logger.debug(f"BrightData data response: {json.dumps(response_data, indent=2)}")
            
            # Process and structure the response
            processed_data = self._process_donation_data(response_data, donor_name)
            
            return {
                "success": True,
                "data": processed_data,
                "query": query,
                "preview_id": preview_id,
                "raw_response": response_data
            }
            
        except httpx.TimeoutException:
            error_msg = "BrightData API request timed out"
            self.logger.error(error_msg)
            raise HTTPException(status_code=504, detail=error_msg)
        except httpx.RequestError as e:
            error_msg = f"BrightData API request error: {str(e)}"
            self.logger.error(error_msg)
            raise HTTPException(status_code=500, detail="Failed to connect to BrightData API")
        except Exception as e:
            error_msg = f"Unexpected error querying BrightData: {str(e)}"
            self.logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    def _process_donation_data(self, raw_data: Dict[str, Any], donor_name: str) -> List[Dict[str, Any]]:
        """
        Process raw BrightData response into structured donation records
        
        Args:
            raw_data: Raw response from BrightData API
            donor_name: Name of the donor
            
        Returns:
            List of processed donation records
        """
        rows = []
        
        try:
            # Log the full response for debugging
            self.logger.info(f"Processing raw BrightData response: {json.dumps(raw_data, indent=2)}")
            
            # The data response contains sample_data array with the actual data
            sample_data = raw_data.get("sample_data", [])
            
            self.logger.info(f"Found {len(sample_data)} items in sample_data")
            
            if not sample_data:
                self.logger.warning("No sample_data found in BrightData response")
                return rows
            
            # Each item contains donation data with filter_results and enrichment_results
            for idx, entry in enumerate(sample_data):
                self.logger.info(f"Processing entry {idx}: {entry.get('name', 'Unknown')}")
                
                # Check if constraint passed (given_by_{donor_name}_check = yes/no)
                filter_results = entry.get("filter_results", [])
                donor_check = "no"
                # Construct the constraint key dynamically based on donor name
                constraint_key = f"given_by_{donor_name.lower().replace(' ', '_')}_check"
                for f in filter_results:
                    if f.get("key") == constraint_key:
                        donor_check = f.get("value", "no").lower()
                        break
                
                # Process all entries (both yes and no results)
                self.logger.info(f"Processing entry {idx} - constraint check: {donor_check}")
                
                # Extract enrichment results (the actual donation data)
                enrichment_results = entry.get("enrichment_results", [])
                row = {
                    "url": entry.get("url"),
                    "name": entry.get("name"),
                    "verification_status": "Verified" if donor_check == "yes" else "Unverified",
                    "recipient": None,
                    "donation_date": None,
                    "donation_amount": None,
                    "donor_identity": None,
                }
                
                # Parse enrichment results
                for enr in enrichment_results:
                    key = enr.get("key")
                    value = enr.get("value")
                    
                    # Skip skipped values
                    if value == "skipped" or not value:
                        continue
                    
                    if key == "recipient":
                        row["recipient"] = value
                    elif key == "donation_date":
                        row["donation_date"] = value
                    elif key == "donation_amount":
                        row["donation_amount"] = value
                    elif key == "donor_identity":
                        row["donor_identity"] = value
                
                self.logger.info(f"Processed row: {json.dumps(row, indent=2)}")
                rows.append(row)
            
            self.logger.info(f"Processed {len(rows)} donation records from BrightData")
            
        except Exception as e:
            self.logger.error(f"Error processing BrightData response: {str(e)}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        return rows
    
    async def get_preview_data(self, preview_id: str) -> Dict[str, Any]:
        """
        Get detailed preview data for a specific preview ID
        
        Args:
            preview_id: The preview ID from an initial query
            
        Returns:
            Dictionary containing the preview data
        """
        
        if not self.api_key:
            self.logger.error("BrightData API key not configured")
            raise HTTPException(status_code=500, detail="BrightData API key not configured")
        
        try:
            headers = self._get_headers()
            preview_url = f"{self.base_url}/preview/{preview_id}"
            
            self.logger.info(f"Fetching preview data from: {preview_url}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(preview_url, headers=headers)
            
            if response.status_code != 200:
                error_msg = f"BrightData preview error: {response.status_code}"
                self.logger.error(error_msg)
                raise HTTPException(status_code=response.status_code, detail=error_msg)
            
            return response.json()
            
        except Exception as e:
            error_msg = f"Error fetching preview data: {str(e)}"
            self.logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
