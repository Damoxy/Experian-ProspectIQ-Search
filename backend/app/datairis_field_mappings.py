"""
DataIris Field Mappings
Maps DataIris API response fields to UI display locations and value transformations
"""

from typing import Dict, Any, Optional

# Income range code mappings
INCOME_RANGE_MAPPING = {
    "1": "Up to $10,000",
    "2": "$10,000 to $14,999",
    "3": "$15,000 to $19,999",
    "4": "$20,000 to $24,999",
    "5": "$25,000 to $29,999",
    "6": "$30,000 to $34,999",
    "7": "$35,000 to $39,999",
    "8": "$40,000 to $44,999",
    "9": "$45,000 to $49,999",
    "A": "$50,000 to $54,999",
    "B": "$55,000 to $59,999",
    "C": "$60,000 to $64,999",
    "D": "$65,000 to $74,999",
    "E": "$75,000 to $99,999",
    "F": "$100,000 to $149,999",
    "G": "$150,000 to $174,999",
    "H": "$175,000 to $199,999",
    "I": "$200,000 to $249,999",
    "J": "$250,000 to $499,999",
    "K": "$500,000 to $999,999",
    "L": "$1,000,000 to $1,999,999",
    "M": "$2,000,000 to $4,999,999",
    "N": "Over $5,000,000",
}

# Home market value code mappings
HOME_MARKET_VALUE_MAPPING = {
    "": "Unknown",
    "A": "Less than $50,000",
    "B": "$50,000 - $99,999",
    "C": "$100,000 - $149,999",
    "D": "$150,000 - $199,999",
    "E": "$200,000 - $249,999",
    "F": "$250,000 - $299,999",
    "G": "$300,000 - $349,999",
    "H": "$350,000 - $399,999",
    "I": "$400,000 - $449,999",
    "J": "$450,000 - $499,999",
    "K": "$500,000 - $599,999",
    "L": "$600,000 - $699,999",
    "M": "$700,000 - $799,999",
    "N": "$800,000 - $999,999",
    "O": "$1,000,000 - $1,499,999",
    "P": "$1,500,000 - $1,999,999",
    "Q": "Greater than $2,000,000",
}

# Net worth code mappings
NETWORTH_CODE_MAPPING = {
    "A": "Up to $30,000",
    "B": "$30,001 to $100,000",
    "C": "$100,001 to $500,000",
    "D": "$500,001 to $1,500,000",
    "E": "Over $1,500,000",
}

# Credit capacity code mappings
CREDIT_CAPACITY_MAPPING = {
    "A": "Under $5,000",
    "B": "$5,000 - $9,999",
    "C": "$10,000 - $24,999",
    "D": "$25,000 - $49,999",
    "E": "$50,000 - $99,999",
    "F": "$100,000 - $249,999",
    "G": "$250,000+",
}

# Donor capacity code mappings
DONOR_CAPACITY_MAPPING = {
    "A": "Up to $499",
    "B": "$500 to $999",
    "C": "$1,000 to $2,499",
    "D": "$2,500 to $4,999",
    "E": "Over $5,000",
}

# Home dwelling type mappings
DWELLING_TYPE_MAPPING = {
    "S": "Single Family Dwelling",
    "C": "Condominium",
    "T": "Townhouse",
    "M": "Mobile Home",
    "F": "Farm",
    "A": "Apartment",
    "O": "Other",
}

# Home owner/renter code mappings
HOME_OWNER_RENTER_MAPPING = {
    "H": "Homeowner",
    "R": "Renter",
    "U": "Unknown",
}

# Gender code mappings
GENDER_MAPPING = {
    "M": "Male",
    "F": "Female",
    "U": "Unknown",
}

# Donor flag mappings (boolean: 1 = yes, empty = no info)
DONOR_FLAG_MAPPING = {
    "1": "Individuals in these households support various causes financially.",
    "": "No information available for this user",
}

# DataIris field to UI mapping
DATAIRIS_UI_MAPPING = {
    # Profile > Overview Section
    "Profile": {
        "Overview": {
            "First_Name": {
                "label": "First Name",
                "type": "text",
                "transformer": None,
            },
            "Last_Name": {
                "label": "Last Name",
                "type": "text",
                "transformer": None,
            },
            "Ind_Age": {
                "label": "Age",
                "type": "number",
                "transformer": None,
            },
            "Ind_Gender_Code": {
                "label": "Gender",
                "type": "mapped",
                "transformer": lambda x: GENDER_MAPPING.get(x, x),
            },
            "Income_Estimated_Household_Ranges": {
                "label": "Estimated Household Income",
                "type": "mapped",
                "transformer": lambda x: INCOME_RANGE_MAPPING.get(x, x),
            },
            "Home_Market_Value": {
                "label": "Home Market Value",
                "type": "mapped",
                "transformer": lambda x: HOME_MARKET_VALUE_MAPPING.get(x, x),
            },
            "NetWorth_Code": {
                "label": "Net Worth",
                "type": "mapped",
                "transformer": lambda x: NETWORTH_CODE_MAPPING.get(x, x),
            },
            "Credit_Capacity_Description": {
                "label": "Credit Capacity",
                "type": "text",
                "transformer": None,
            },
            "Donor_Capacity_Code": {
                "label": "Capacity Range $",
                "type": "mapped",
                "transformer": lambda x: DONOR_CAPACITY_MAPPING.get(x, x),
            },
            "Marital_Status_Code": {
                "label": "Marital Status",
                "type": "text",
                "transformer": None,
            },
        },
        "Contact": {
            "Physical_Address": {
                "label": "Address",
                "type": "text",
                "transformer": None,
            },
            "Physical_City": {
                "label": "City",
                "type": "text",
                "transformer": None,
            },
            "Physical_State": {
                "label": "State",
                "type": "text",
                "transformer": None,
            },
            "Physical_Zip": {
                "label": "Zip Code",
                "type": "text",
                "transformer": None,
            },
            "Phone": {
                "label": "Phone Number",
                "type": "phone",
                "transformer": None,
            },
            "Email": {
                "label": "Email",
                "type": "email",
                "transformer": None,
            },
            "Area_Code": {
                "label": "Area Code",
                "type": "text",
                "transformer": None,
            },
        },
        "Home": {
            "Home_Dwelling_Type_Code": {
                "label": "Dwelling Type",
                "type": "mapped",
                "transformer": lambda x: DWELLING_TYPE_MAPPING.get(x, x),
            },
            "Home_Owner_Renter_Code": {
                "label": "Owner/Renter",
                "type": "mapped",
                "transformer": lambda x: HOME_OWNER_RENTER_MAPPING.get(x, x),
            },
            "Home_Built_Year_Code": {
                "label": "Year Built",
                "type": "text",
                "transformer": None,
            },
            "Home_Square_Footage": {
                "label": "Square Footage",
                "type": "number",
                "transformer": None,
            },
            "Length_Of_Residence_Code": {
                "label": "Length of Residence",
                "type": "text",
                "transformer": None,
            },
            "Unit_Type": {
                "label": "Unit Type",
                "type": "text",
                "transformer": None,
            },
            "Unit_Number": {
                "label": "Unit Number",
                "type": "text",
                "transformer": None,
            },
        },
        "Location": {
            "Latitude": {
                "label": "Latitude",
                "type": "number",
                "transformer": None,
            },
            "Longitude": {
                "label": "Longitude",
                "type": "number",
                "transformer": None,
            },
            "CBSA_Code": {
                "label": "CBSA Code",
                "type": "text",
                "transformer": None,
            },
        },
    },
    
    # Profile > Interests Section
    "Interests": {
        "Hobbies": {
            "Hobby_Interest": {
                "label": "Hobbies",
                "type": "array",
                "transformer": None,
            },
            "Reading": {
                "label": "Reading Interests",
                "type": "array",
                "transformer": None,
            },
            "Outdoor_Enthusiast": {
                "label": "Outdoor Enthusiast",
                "type": "boolean",
                "transformer": lambda x: x == "1" if x else False,
            },
        },
        "Lifestyle": {
            "Green_Living": {
                "label": "Green Living",
                "type": "boolean",
                "transformer": lambda x: x == "1" if x else False,
            },
            "Consumer_Electronics": {
                "label": "Consumer Electronics",
                "type": "text",
                "transformer": None,
            },
            "Computers": {
                "label": "Computers",
                "type": "text",
                "transformer": None,
            },
        },
        "Arts & Culture": {
            "Arts_History_Science": {
                "label": "Arts/History/Science",
                "type": "text",
                "transformer": None,
            },
            "Beauty_Fashion": {
                "label": "Beauty & Fashion",
                "type": "array",
                "transformer": None,
            },
        },
    },
    
    # Profile > Donor Info Section
    "DonorInfo": {
        "Capacity": {
        },
    },
    
    # Philanthropy Section
    "Philanthropy": {
        "Giving Categories of Interest": {
            "Donor_Political_Flag": {
                "label": "Political Causes",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Health_Flag": {
                "label": "Health Causes",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Charitable_Flag": {
                "label": "Charitable Causes",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Veterans_Flag": {
                "label": "Veterans Causes",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Animal_Welfare_Flag": {
                "label": "Animal Welfare",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Arts_Cultural_Flag": {
                "label": "Arts & Cultural",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Political_Conservative_Flag": {
                "label": "Political Conservative",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Childrens_Flag": {
                "label": "Children's Causes",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Religious_Flag": {
                "label": "Religious Causes",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_International_Aid_Flag": {
                "label": "International Aid",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Environmental_Wildlife_Flag": {
                "label": "Environmental & Wildlife",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
            "Donor_Political_Liberal_Flag": {
                "label": "Political Liberal",
                "type": "mapped",
                "transformer": lambda x: DONOR_FLAG_MAPPING.get(x, "No information available for this user"),
            },
        },
    },
}


def transform_datairis_field(field_id: str, field_value: str, section: Optional[str] = None) -> Dict[str, Any]:
    """
    Transform a DataIris field into a UI-ready format
    
    Args:
        field_id: The DataIris field ID (e.g., "Income_Estimated_Household_Ranges")
        field_value: The raw field value from API
        section: Optional section name to narrow down mapping
    
    Returns:
        dict: Transformed field with label, value, and metadata
    """
    # Search through mapping to find the field
    for category, subcategories in DATAIRIS_UI_MAPPING.items():
        for sub_category, fields in subcategories.items():
            if field_id in fields:
                field_config = fields[field_id]
                
                # Apply transformer if provided
                transformed_value = field_value
                if field_config.get("transformer"):
                    try:
                        transformed_value = field_config["transformer"](field_value)
                    except Exception as e:
                        print(f"Error transforming {field_id}: {e}")
                        transformed_value = field_value
                
                return {
                    "field_id": field_id,
                    "label": field_config.get("label"),
                    "value": transformed_value,
                    "type": field_config.get("type"),
                    "category": category,
                    "subcategory": sub_category,
                }
    
    # Field not found in mapping
    return {
        "field_id": field_id,
        "label": field_id.replace("_", " "),
        "value": field_value,
        "type": "text",
        "category": "Other",
        "subcategory": "Unmapped",
    }


def transform_datairis_results(results: list) -> Dict[str, Any]:
    """
    Transform raw DataIris results into UI-ready format organized by sections.
    Always pre-populates Philanthropy and Profile Overview fields with defaults.
    
    Args:
        results: List of parsed DataIris records
    
    Returns:
        dict: Organized results by category and subcategory
    """
    organized_results = {}
    philanthropy_fields = []
    
    # Always initialize Philanthropy section with all 11 fields
    organized_results["Philanthropy"] = {}
    organized_results["Philanthropy"]["Giving Categories of Interest"] = []
    
    # Pre-populate all Philanthropy fields with default "No information" message
    for field_id, field_config in DATAIRIS_UI_MAPPING["Philanthropy"]["Giving Categories of Interest"].items():
        organized_results["Philanthropy"]["Giving Categories of Interest"].append({
            "label": field_config.get("label"),
            "value": "No information available for this user",
            "type": field_config.get("type"),
        })
    
    # Always initialize Profile > Overview section with key financial fields
    organized_results["Profile"] = {}
    organized_results["Profile"]["Overview"] = []
    
    # Pre-populate Profile Overview fields with default "No information" message
    profile_overview_fields = ["Donor_Capacity_Code", "Income_Estimated_Household_Ranges", "Home_Market_Value", "NetWorth_Code"]
    for field_id in profile_overview_fields:
        if field_id in DATAIRIS_UI_MAPPING["Profile"]["Overview"]:
            field_config = DATAIRIS_UI_MAPPING["Profile"]["Overview"][field_id]
            organized_results["Profile"]["Overview"].append({
                "label": field_config.get("label"),
                "value": "No information available for this user",
                "type": field_config.get("type"),
            })
    
    # If no results, return with all fields showing "No information"
    if not results or len(results) == 0:
        return organized_results
    
    # Process actual results - override the "No information" defaults with real data
    for record in results:
        for field_id, field_value in record.items():
            # Special handling for Philanthropy fields - include even if empty
            is_philanthropy_field = (
                (field_id.startswith('Donor_') and field_id.endswith('_Flag')) or
                field_id in ['Animal_Welfare_Flag', 'Arts_Cultural_Flag']
            )
            
            # Special handling for Profile Overview fields - include even if empty
            is_profile_overview_field = field_id in profile_overview_fields
            
            if not field_value and not is_philanthropy_field and not is_profile_overview_field:
                continue
            
            transformed = transform_datairis_field(field_id, field_value)
            category = transformed["category"]
            subcategory = transformed["subcategory"]
            
            if category == "Philanthropy":
                philanthropy_fields.append(field_id)
                # Find and replace the default "No information" with actual value
                for item in organized_results["Philanthropy"]["Giving Categories of Interest"]:
                    if item["label"] == transformed["label"]:
                        item["value"] = transformed["value"]
                        break
            elif category == "Profile" and subcategory == "Overview" and field_id in profile_overview_fields:
                # Find and replace the default "No information" with actual value for Profile Overview
                for item in organized_results["Profile"]["Overview"]:
                    if item["label"] == transformed["label"]:
                        item["value"] = transformed["value"]
                        break
            else:
                # Initialize structure if needed for other fields
                if category not in organized_results:
                    organized_results[category] = {}
                if subcategory not in organized_results[category]:
                    organized_results[category][subcategory] = []
                
                # Add transformed field
                organized_results[category][subcategory].append({
                    "label": transformed["label"],
                    "value": transformed["value"],
                    "type": transformed["type"],
                })
    
    if philanthropy_fields:
        print(f"[DEBUG] Found Philanthropy fields: {philanthropy_fields}")
    
    return organized_results
