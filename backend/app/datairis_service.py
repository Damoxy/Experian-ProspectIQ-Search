"""
DataIris Service Module
Handles integration with DataIris API for prospect searching
"""

import requests
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from datairis_field_mappings import transform_datairis_results, transform_datairis_field


class DataIrisService:
    """Service for interacting with DataIris API"""
    
    def __init__(self, db_session=None):
        """Initialize DataIris service with environment variables"""
        load_dotenv()
        
        self.base_url = os.getenv("DATAIRIS_BASE_URL", "https://www.datairis.co/V1")
        self.account_username = os.getenv("DATAIRIS_ACCOUNT_USERNAME")
        self.account_password = os.getenv("DATAIRIS_ACCOUNT_PASSWORD")
        self.subscriber_id = os.getenv("DATAIRIS_SUBSCRIBER_ID")
        self.subscriber_username = os.getenv("DATAIRIS_SUBSCRIBER_USERNAME")
        self.subscriber_password = os.getenv("DATAIRIS_SUBSCRIBER_PASSWORD")
        self.access_token = os.getenv("DATAIRIS_ACCESS_TOKEN")
        
        self.db_session = db_session
        self.token_id = None
    
    def authenticate(self) -> Optional[str]:
        """
        Authenticate with DataIris API and get TokenID
        
        Returns:
            str: TokenID for subsequent requests, None if failed
        """
        url = f"{self.base_url}/auth/subscriber/"
        headers = {
            "SubscriberID": self.subscriber_id,
            "subscriberUsername": self.subscriber_username,
            "SubscriberPassword": self.subscriber_password,
            "AccountUsername": self.account_username,
            "AccountPassword": self.account_password,
            "AccountDetailsRequired": "true"
        }
        params = {"AccessToken": self.access_token}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for errors
            if "ERROR" in data.get("Response", {}).get("responseDetails", {}):
                print(f"Authentication Error: {data['Response']['responseDetails']['ERROR']}")
                return None
            
            self.token_id = data["Response"]["responseDetails"].get("TokenID")
            return self.token_id
            
        except requests.exceptions.RequestException as e:
            print(f"Authentication request failed: {str(e)}")
            return None
    
    def reset_criteria(self) -> bool:
        """
        Reset search criteria for a new search
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.token_id:
            print("Not authenticated. Call authenticate() first.")
            return False
        
        url = f"{self.base_url}/criteria/search/deleteall/consumer"
        headers = {"TokenID": self.token_id}
        
        try:
            response = requests.delete(url, headers=headers, timeout=30)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Reset criteria failed: {str(e)}")
            return False
    
    def add_search_criteria(self, first_name: str, last_name: str, zip_code: str) -> bool:
        """
        Add search criteria to DataIris API
        
        Args:
            first_name: Person's first name
            last_name: Person's last name
            zip_code: Person's zip code
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.token_id:
            print("Not authenticated. Call authenticate() first.")
            return False
        
        url = f"{self.base_url}/criteria/search/addall/consumer"
        headers = {
            "TokenID": self.token_id,
            "Content-Type": "application/json"
        }
        
        criteria = {
            "First_Name": first_name,
            "Last_Name": last_name,
            "Physical_Zip": zip_code
        }
        
        try:
            response = requests.put(url, headers=headers, json=criteria, timeout=30)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Add criteria failed: {str(e)}")
            return False
    
    def search(self, first_name: str, last_name: str, zip_code: str, 
               start: int = 1, end: int = 10) -> Optional[Dict]:
        """
        Complete search workflow: check cache -> authenticate, set criteria, and get results
        
        Args:
            first_name: Person's first name
            last_name: Person's last name
            zip_code: Person's zip code
            start: Start record number (default 1)
            end: End record number (default 10)
        
        Returns:
            dict: Search results or None if failed
        """
        # Check cache first if db_session is available
        if self.db_session:
            from services.datairis_cache_service import DataIrisCacheService
            cached_result = DataIrisCacheService.find_cached_result(
                self.db_session,
                first_name=first_name,
                last_name=last_name,
                zip_code=zip_code
            )
            if cached_result:
                print(f"[INFO] DataIris cache HIT for {first_name} {last_name} {zip_code}")
                return cached_result
            print(f"[DEBUG] DataIris cache MISS for {first_name} {last_name} {zip_code}")
        
        # Step 1: Authenticate
        if not self.authenticate():
            return None
        
        # Step 2: Reset criteria
        if not self.reset_criteria():
            return None
        
        # Step 3: Add search criteria
        if not self.add_search_criteria(first_name, last_name, zip_code):
            return None
        
        # Step 4: Get records
        raw_results = self.get_records(start, end)
        print(f"[DEBUG] Raw results from API: {raw_results}")
        
        # Parse and transform results
        transformed_results = None
        parsed_records = self.parse_results(raw_results) if raw_results else []
        record_count = len(parsed_records)
        
        # Always transform results, even if empty (will populate default Philanthropy fields)
        transformed_results = transform_datairis_results(parsed_records)
        print(f"[DEBUG] Transformed results: {len(transformed_results)} categories, record_count: {record_count}")
        
        # Save to cache ONLY if we have transformed results
        if self.db_session and transformed_results:
            from services.datairis_cache_service import DataIrisCacheService
            DataIrisCacheService.save_cache_result(
                self.db_session,
                search_response=raw_results,
                transformed_results=transformed_results,
                first_name=first_name,
                last_name=last_name,
                zip_code=zip_code,
                record_count=record_count,
                is_partial=False
            )
        elif self.db_session and not transformed_results:
            print(f"[INFO] Skipping cache save - no transformed results for {first_name} {last_name} {zip_code}")
        
        return {
            "search_response": raw_results,
            "transformed_results": transformed_results
        }
    
    def get_records(self, start: int = 1, end: int = 10) -> Optional[Dict]:
        """
        Get search results from DataIris API
        
        Args:
            start: Start record number (default 1)
            end: End record number (default 10)
        
        Returns:
            dict: Search results or None if failed
        """
        if not self.token_id:
            print("Not authenticated. Call authenticate() first.")
            return None
        
        url = f"{self.base_url}/search/consumer"
        headers = {"TokenID": self.token_id}
        params = {"Start": start, "End": end}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            raw_response = response.json()
            
            # Extract the SearchResult from nested response structure
            # Response structure: {'Response': {'responseDetails': {'SearchResult': {...}}}}
            if 'Response' in raw_response and 'responseDetails' in raw_response['Response']:
                search_result = raw_response['Response']['responseDetails'].get('SearchResult')
                if search_result:
                    return search_result
            
            # Fallback to raw response if structure is different
            return raw_response
            
        except requests.exceptions.RequestException as e:
            print(f"Get records failed: {str(e)}")
            return None
    
    def parse_results(self, results: Dict) -> List[Dict]:
        """
        Parse raw API results into a more usable format
        
        Args:
            results: Raw API response (SearchResult structure)
        
        Returns:
            list: List of parsed records with field names as keys
        """
        parsed_records = []
        
        if not results:
            print("[DEBUG] parse_results - Results is empty/None")
            return parsed_records
        
        if "searchResultRecord" not in results:
            print(f"[DEBUG] parse_results - No 'searchResultRecord' key found. Available keys: {list(results.keys())}")
            return parsed_records
        
        search_records = results.get("searchResultRecord")
        print(f"[DEBUG] parse_results - Found searchResultRecord with {len(search_records)} records")
        
        for record in search_records:
            parsed_record = {}
            
            if "resultFields" in record:
                for field in record["resultFields"]:
                    field_id = field.get("fieldID")
                    field_value = field.get("fieldValue")
                    parsed_record[field_id] = field_value
            
            if parsed_record:  # Only add non-empty records
                parsed_records.append(parsed_record)
        
        print(f"[DEBUG] parse_results - Parsed {len(parsed_records)} total records")
        return parsed_records
    
    def parse_and_transform_results(self, results: Dict) -> Dict:
        """
        Parse raw API results and transform them into UI-ready format
        
        Args:
            results: Raw API response
        
        Returns:
            dict: Organized and transformed results by category
        """
        parsed_records = self.parse_results(results)
        return transform_datairis_results(parsed_records)


# Available data fields from DataIris API
DATAIRIS_FIELD_MAPPING = {
    # Personal Information
    "First_Name": "First Name",
    "Last_Name": "Last Name",
    "Middle_Initial": "Middle Initial",
    "Ind_Age": "Age",
    "Age_Advanced": "Age (Advanced)",
    "Ind_Gender_Code": "Gender Code",
    "Marital_Status_Code": "Marital Status Code",
    
    # Contact Information
    "Physical_Address": "Physical Address",
    "Physical_City": "City",
    "Physical_State": "State",
    "Physical_Zip": "Zip Code",
    "Phone": "Phone Number",
    "Area_Code": "Area Code",
    "Email": "Email",
    
    # Geographic Information
    "Latitude": "Latitude",
    "Longitude": "Longitude",
    "CBSA_Code": "CBSA Code",
    "Vendor_State_County": "County Code",
    "Tally_County_Code": "Tally County Code",
    "Physical_State_Physical_City": "State City",
    
    # Home Information
    "Home_Dwelling_Type_Code": "Dwelling Type",
    "Home_Owner_Renter_Code": "Home Owner/Renter",
    "Home_Built_Year_Code": "Home Built Year",
    "Home_Market_Value": "Home Market Value",
    "Home_Purchase_Date": "Home Purchase Date",
    "Home_Square_Footage": "Home Square Footage",
    "Home_Year_Built_Code": "Home Year Built Code",
    "Home_Recent_Buyer_Flag": "Recent Buyer Flag",
    "Home_Equity_Available_Code": "Home Equity Available",
    "Home_Loan_To_Value_Code": "Loan to Value",
    "Unit_Number": "Unit Number",
    "Unit_Type": "Unit Type",
    
    # Income & Wealth
    "Income_Estimated_Household_Ranges": "Income Range",
    "Median_Home_Income_Code": "Median Home Income",
    "Median_Home_Value_Code": "Median Home Value",
    "Credit_Capacity": "Credit Capacity",
    "Credit_Capacity_Code": "Credit Capacity Code",
    "Credit_Capacity_Description": "Credit Capacity Description",
    "NetWorth_Code": "Net Worth Code",
    
    # Donor Information
    "Donor_Capacity_Code": "Donor Capacity",
    "Donor_Political_Flag": "Political Donor",
    "Donor_Political_Conservative_Flag": "Conservative Political Donor",
    "Donor_Political_Liberal_Flag": "Liberal Political Donor",
    "Donor_Charitable_Flag": "Charitable Donor",
    "Donor_Religious_Flag": "Religious Donor",
    "Donor_Health_Flag": "Health Donor",
    "Donor_Environmental_Wildlife_Flag": "Environmental/Wildlife Donor",
    "Donor_International_Aid_Flag": "International Aid Donor",
    "Donor_Childrens_Flag": "Children's Donor",
    "Donor_Veterans_Flag": "Veterans Donor",
    "Donor_Arts_Cultural_Flag": "Arts/Cultural Donor",
    
    # Interests & Hobbies
    "Hobby_Interest": "Hobby Interests",
    "Reading": "Reading Interests",
    "Arts_History_Science": "Arts/History/Science",
    "Beauty_Fashion": "Beauty/Fashion",
    "Computers": "Computers",
    "Consumer_Electronics": "Consumer Electronics",
    "Collectibles_Antiques": "Collectibles/Antiques",
    "Childrens": "Children's Interests",
    "Animal_Welfare_Flag": "Animal Welfare Interest",
    "Outdoor_Enthusiast": "Outdoor Enthusiast",
    "Green_Living": "Green Living",
    "Family_Religion_Politics": "Family/Religion/Politics",
    "Arts_Cultural_Flag": "Arts/Cultural Interest",
    
    # Other Information
    "Length_Of_Residence_Code": "Length of Residence",
    "Location_Unique": "Location Unique",
    "Scrubbed_Phoneable_Flag": "Phoneable Flag",
    "Email_Present_Flag": "Email Present Flag",
    "Suppression_Flag": "Suppression Flag",
    "Vehicle_Owned_Code": "Vehicle Owned",
    "Id": "ID",
    "DatabaseUSA_Household_ID": "Household ID",
}
