"""
KnowledgeCore database service - handles database-first search operations
"""

import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from database import Donor, get_givingtrend_db
from models import SearchRequest
from core.logging_config import setup_logging
from config import DEBUG


class KnowledgeCoreService:
    """Service class for handling KnowledgeCore database operations"""
    
    def __init__(self):
        self.logger = setup_logging(DEBUG)
    
    def normalize_zip_code(self, zip_code: str) -> str:
        """Extract first 5 digits from ZIP code (handles format like 54113-1247)"""
        if not zip_code:
            return ""
        # Remove any non-digit characters and take first 5 digits
        digits_only = ''.join(c for c in zip_code if c.isdigit())
        return digits_only[:5] if len(digits_only) >= 5 else digits_only
    
    def normalize_address(self, address: str) -> str:
        """Normalize address for comparison"""
        if not address:
            return ""
        
        # Convert to uppercase and remove extra spaces
        normalized = ' '.join(address.upper().split())
        
        # Common abbreviation replacements for better matching
        abbreviations = {
            ' STREET': ' ST',
            ' DRIVE': ' DR',
            ' AVENUE': ' AVE',
            ' BOULEVARD': ' BLVD',
            ' ROAD': ' RD',
            ' LANE': ' LN',
            ' COURT': ' CT',
            ' PLACE': ' PL',
            ' CIRCLE': ' CIR',
            ' TRAIL': ' TRL'
        }
        
        for full, abbrev in abbreviations.items():
            normalized = normalized.replace(full, abbrev)
        
        return normalized
    
    async def search_donors(self, search_request: SearchRequest, db: Session) -> List[Dict[str, Any]]:
        """
        Search for donors in KnowledgeCore database
        
        Args:
            search_request: The search parameters from the frontend
            db: Database session
            
        Returns:
            List of matching donor records
        """
        try:
            self.logger.info(f"Searching KnowledgeCore database for: {search_request.FIRST_NAME} {search_request.LAST_NAME}")
            
            # Normalize input ZIP code to first 5 digits
            search_zip = self.normalize_zip_code(search_request.ZIP)
            
            # Build base query
            query = db.query(Donor)
            
            # Apply filters - case insensitive matching
            filters = []
            
            # Name filters (required)
            if search_request.FIRST_NAME:
                filters.append(func.upper(Donor.REFirstName).like(f"%{search_request.FIRST_NAME.upper()}%"))
            
            if search_request.LAST_NAME:
                filters.append(func.upper(Donor.RELastName).like(f"%{search_request.LAST_NAME.upper()}%"))
            
            # ZIP code filter (compare first 5 digits)
            if search_zip:
                filters.append(func.left(Donor.REZipCode, 5) == search_zip)
            
            # Apply all filters with AND logic
            if filters:
                query = query.filter(and_(*filters))
            
            # Execute query and limit results to prevent overwhelming responses
            results = query.limit(50).all()
            
            self.logger.info(f"Found {len(results)} matches in KnowledgeCore database")
            
            # Convert results to dictionaries
            donor_records = []
            for donor in results:
                # Calculate address similarity score for ranking
                donor_address = self.normalize_address(donor.ReAddress or "")
                search_address = self.normalize_address(search_request.STREET1)
                
                # Simple similarity check - contains key parts
                address_score = 0
                if donor_address and search_address:
                    # Split into components and check for matches
                    donor_parts = donor_address.split()
                    search_parts = search_address.split()
                    
                    matches = sum(1 for part in search_parts if part in donor_parts)
                    address_score = matches / len(search_parts) if search_parts else 0
                
                donor_record = {
                    "first_name": donor.REFirstName or "",
                    "middle_name": donor.REMiddleName or "",
                    "last_name": donor.RELastName or "",
                    "address": donor.ReAddress or "",
                    "city": donor.RECity or "",
                    "state": donor.REState or "",
                    "zip_code": donor.REZipCode or "",
                    "constituent_id": donor.ConstituentId or "",
                    "phone": donor.REPhone or "",
                    "email": donor.REEmail or "",
                    "address_match_score": round(address_score, 2),
                    "source": "KnowledgeCore_Database"
                }
                donor_records.append(donor_record)
            
            # Sort by address match score (best matches first)
            donor_records.sort(key=lambda x: x["address_match_score"], reverse=True)
            
            return donor_records
            
        except Exception as e:
            self.logger.error(f"Error searching KnowledgeCore database: {str(e)}")
            return []
    
    def format_consumer_behavior_response(self, donors: List[Dict[str, Any]], search_request: SearchRequest) -> Dict[str, Any]:
        """
        Format database results to match the expected Experian API response structure
        
        Args:
            donors: List of donor records from database
            search_request: Original search request
            
        Returns:
            Formatted response matching Experian API structure
        """
        if not donors:
            return {
                "message": "No records found in KnowledgeCore database",
                "source": "database",
                "results": {
                    "consumer_behavior": {
                        "summary": {
                            "total_records": 0,
                            "search_criteria": {
                                "first_name": search_request.FIRST_NAME,
                                "last_name": search_request.LAST_NAME,
                                "address": f"{search_request.STREET1}, {search_request.CITY}, {search_request.STATE} {search_request.ZIP}"
                            }
                        },
                        "records": []
                    }
                }
            }
        
        # Format donor records for consumer behavior section
        formatted_records = []
        for donor in donors:
            formatted_record = {
                "personal_info": {
                    "first_name": donor["first_name"],
                    "middle_name": donor["middle_name"],
                    "last_name": donor["last_name"],
                    "full_name": f"{donor['first_name']} {donor['middle_name']} {donor['last_name']}".strip()
                },
                "address_info": {
                    "street_address": donor["address"],
                    "city": donor["city"],
                    "state": donor["state"],
                    "zip_code": donor["zip_code"],
                    "full_address": f"{donor['address']}, {donor['city']}, {donor['state']} {donor['zip_code']}"
                },
                "contact_info": {
                    "constituent_id": donor["constituent_id"],
                    "phone": donor["phone"],
                    "email": donor["email"]
                },
                "match_quality": {
                    "address_similarity": donor["address_match_score"],
                    "confidence_level": "High" if donor["address_match_score"] > 0.7 else "Medium" if donor["address_match_score"] > 0.3 else "Low"
                },
                "data_source": "KnowledgeCore Database",
                "record_type": "Donor Profile"
            }
            formatted_records.append(formatted_record)
        
        return {
            "message": f"Found {len(donors)} records in KnowledgeCore database",
            "source": "database",
            "results": {
                "consumer_behavior": {
                    "summary": {
                        "total_records": len(donors),
                        "search_criteria": {
                            "first_name": search_request.FIRST_NAME,
                            "last_name": search_request.LAST_NAME,
                            "address": f"{search_request.STREET1}, {search_request.CITY}, {search_request.STATE} {search_request.ZIP}"
                        },
                        "data_source": "KnowledgeCore_GivingTrendDB_test.dbo.Donor",
                        "match_types": ["Name Match", "ZIP Code Match", "Address Similarity"]
                    },
                    "records": formatted_records
                }
            }
        }