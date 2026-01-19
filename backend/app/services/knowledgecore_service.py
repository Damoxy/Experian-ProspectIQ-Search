"""
KnowledgeCore database service - handles database-first search operations
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, distinct, text
from database import Constituent, Transaction, get_givingtrend_db
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
    
    def format_currency(self, amount_str: str) -> str:
        """
        Format currency string with commas for thousands
        Handles various input formats ($1000.00, 1000.00, 1000, etc.)
        
        Args:
            amount_str: Amount as string
            
        Returns:
            Formatted amount string with commas
        """
        try:
            # Remove $ and commas, convert to float
            cleaned = str(amount_str).replace('$', '').replace(',', '').strip()
            amount = float(cleaned)
            # Format with commas and 2 decimal places
            return f"${amount:,.2f}"
        except (ValueError, TypeError):
            return amount_str
    
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
    
    def calculate_gift_metrics(self, constituent_id: str, db: Session) -> Dict[str, Any]:
        """
        Calculate gift metrics from Transaction table for a given constituent
        
        Args:
            constituent_id: The constituent ID to search for
            db: Database session
            
        Returns:
            Dictionary containing gift metrics with dates
        """
        try:
            self.logger.info(f"Calculating gift metrics for constituent_id: {constituent_id}")
            
            # Use raw SQL query to avoid ORM deduplication issues with composite primary keys
            # The ORM can filter out duplicate rows with same (Constituent_ID, Gift_Date) pair
            import os
            
            gt_db_name = os.getenv("KC_GT_DB_DATABASE")
            
            query = text(f"""
            SELECT 
                Gift_Date,
                Gift_Amount,
                Gift_Type,
                Gift_Pledge_Balance
            FROM [{gt_db_name}].[dbo].[Transaction]
            WHERE Constituent_ID = :constituent_id
            ORDER BY Gift_Date DESC
            """)
            
            result = db.execute(query, {"constituent_id": constituent_id})
            transactions = result.fetchall()
            
            self.logger.info(f"Found {len(transactions)} total transactions for constituent_id: {constituent_id}")
            
            if not transactions:
                return {
                    "lifetime_giving": "No transactions found",
                    "largest_gift": "No transactions found",
                    "first_gift": "No transactions found", 
                    "latest_gift": "No transactions found"
                }
            
            # Convert gift amounts to float for calculations (handle various formats)
            valid_transactions = []
            invalid_count = 0
            for trans in transactions:
                try:
                    # Clean and convert gift amount
                    amount_str = str(trans.Gift_Amount).replace('$', '').replace(',', '').strip()
                    self.logger.debug(f"Processing transaction: Date={trans.Gift_Date}, Original={trans.Gift_Amount}, Cleaned={amount_str}")
                    
                    if amount_str and amount_str not in ['', 'None', 'NULL']:
                        amount = float(amount_str)
                        if amount > 0:  # Only positive amounts
                            valid_transactions.append({
                                'amount': amount,
                                'date': trans.Gift_Date,
                                'original_amount': trans.Gift_Amount
                            })
                            self.logger.debug(f"[VALID] Transaction added: ${amount:,.2f}")
                        else:
                            self.logger.debug(f"[SKIP] Negative/zero amount: ${amount:,.2f}")
                            invalid_count += 1
                    else:
                        self.logger.debug(f"[SKIP] Empty/NULL amount string")
                        invalid_count += 1
                except (ValueError, TypeError) as e:
                    self.logger.debug(f"[SKIP] Parse error: {str(e)}")
                    invalid_count += 1
                    continue
            
            self.logger.info(f"Valid transactions: {len(valid_transactions)}, Invalid/Skipped: {invalid_count}")
            
            if not valid_transactions:
                return {
                    "lifetime_giving": "No valid transactions",
                    "largest_gift": "No valid transactions",
                    "first_gift": "No valid transactions",
                    "latest_gift": "No valid transactions"
                }
            
            # Calculate metrics
            total_giving = sum(t['amount'] for t in valid_transactions)
            
            self.logger.info(f"Lifetime giving for constituent_id {constituent_id}: ${total_giving:,.2f} (from {len(valid_transactions)} valid transactions)")
            
            # Find largest gift
            largest = max(valid_transactions, key=lambda x: x['amount'])
            
            # Find first gift (earliest date)
            first = min(valid_transactions, key=lambda x: x['date'] if x['date'] else datetime.min)
            
            # Find latest gift (most recent date)
            latest = max(valid_transactions, key=lambda x: x['date'] if x['date'] else datetime.min)
            
            # Format results
            return {
                "lifetime_giving": f"${total_giving:,.2f}",
                "largest_gift": f"{self.format_currency(largest['original_amount'])} ({largest['date'].strftime('%m/%d/%Y') if largest['date'] else 'No date'})",
                "first_gift": f"{self.format_currency(first['original_amount'])} ({first['date'].strftime('%m/%d/%Y') if first['date'] else 'No date'})",
                "latest_gift": f"{self.format_currency(latest['original_amount'])} ({latest['date'].strftime('%m/%d/%Y') if latest['date'] else 'No date'})"
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating gift metrics for constituent {constituent_id}: {str(e)}")
            return {
                "lifetime_giving": "Error calculating",
                "largest_gift": "Error calculating",
                "first_gift": "Error calculating",
                "latest_gift": "Error calculating"
            }
    
    async def search_donors(self, search_request: SearchRequest, db: Session) -> List[Dict[str, Any]]:
        """
        Search for constituents in KnowledgeCore database using Constituent table
        
        Args:
            search_request: The search parameters from the frontend
            db: Database session
            
        Returns:
            List of matching constituent records with distinct ConstituentID
        """
        try:
            self.logger.info(f"Searching KnowledgeCore database for: {search_request.FIRST_NAME} {search_request.LAST_NAME}")
            
            # Normalize input ZIP code to first 5 digits
            search_zip = self.normalize_zip_code(search_request.ZIP)
            
            # Build base query - select distinct Constituent_ID to handle multiple results per constituent
            query = db.query(Constituent).distinct(Constituent.Constituent_ID)
            
            # Apply filters - case insensitive matching
            filters = []
            
            # Name filters (required)
            if search_request.FIRST_NAME:
                filters.append(func.upper(Constituent.First_Name).like(f"%{search_request.FIRST_NAME.upper()}%"))
            
            if search_request.LAST_NAME:
                filters.append(func.upper(Constituent.Last_Name).like(f"%{search_request.LAST_NAME.upper()}%"))
            
            # ZIP code filter (compare first 5 digits)
            if search_zip:
                filters.append(func.left(Constituent.Preferred_ZIP, 5) == search_zip)
            
            # Apply all filters with AND logic
            if filters:
                query = query.filter(and_(*filters))
            
            # Execute query and limit results to prevent overwhelming responses
            results = query.limit(50).all()
            
            self.logger.info(f"Found {len(results)} matches in KnowledgeCore database")
            
            # Convert results to dictionaries
            constituent_records = []
            for constituent in results:
                # Calculate address similarity score for ranking
                constituent_address = self.normalize_address(constituent.Preferred_Address_Line_1 or "")
                search_address = self.normalize_address(search_request.STREET1)
                
                # Simple similarity check - contains key parts
                address_score = 0
                if constituent_address and search_address:
                    # Split into components and check for matches
                    constituent_parts = constituent_address.split()
                    search_parts = search_address.split()
                    
                    matches = sum(1 for part in search_parts if part in constituent_parts)
                    address_score = matches / len(search_parts) if search_parts else 0
                
                constituent_record = {
                    "first_name": constituent.First_Name or "",
                    "last_name": constituent.Last_Name or "",
                    "address": constituent.Preferred_Address_Line_1 or "",
                    "city": constituent.Preferred_City or "",
                    "state": constituent.Preferred_State or "",
                    "zip_code": constituent.Preferred_ZIP or "",
                    "constituent_id": constituent.Constituent_ID or "",
                    "phone": constituent.Preferred_Home_Phone_Number or "",
                    "email": constituent.Preferred_E_mail_Number or "",
                    "address_match_score": round(address_score, 2),
                    "source": "KnowledgeCore_Database"
                }
                constituent_records.append(constituent_record)
            
            # Sort by address match score (best matches first)
            constituent_records.sort(key=lambda x: x["address_match_score"], reverse=True)
            
            return constituent_records
            
        except Exception as e:
            self.logger.error(f"Error searching KnowledgeCore database: {str(e)}")
            return []
    
    def format_consumer_behavior_response(self, donors: List[Dict[str, Any]], search_request: SearchRequest, db: Session = None) -> Dict[str, Any]:
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
            # Calculate gift metrics if database session is available
            gift_metrics = {}
            if db and donor["constituent_id"]:
                gift_metrics = self.calculate_gift_metrics(donor["constituent_id"], db)
            
            # Prepare contact_info with gift metrics
            contact_info = {
                "constituent_id": donor["constituent_id"],
                "phone": donor["phone"],
                "email": donor["email"]
            }
            
            # Add gift metrics if available
            if gift_metrics:
                contact_info.update(gift_metrics)
            
            formatted_record = {
                "personal_info": {
                    "first_name": donor["first_name"],
                    "last_name": donor["last_name"],
                    "full_name": f"{donor['first_name']} {donor['last_name']}".strip()
                },
                "address_info": {
                    "street_address": donor["address"],
                    "city": donor["city"],
                    "state": donor["state"],
                    "zip_code": donor["zip_code"],
                    "full_address": f"{donor['address']}, {donor['city']}, {donor['state']} {donor['zip_code']}"
                },
                "contact_info": contact_info,
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