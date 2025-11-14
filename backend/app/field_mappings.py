"""
Field mappings for Experian API response transformation
"""

from typing import Dict, Any

# Comprehensive field mappings for user-friendly names
FIELD_MAPPINGS: Dict[str, str] = {
    # Message and General Info
    "ELSGenericMessage.Message.TYPE": "Message Type",
    "ELSGenericMessage.Message.STATUS": "Status",
    "ELSGenericMessage.Message.CODE": "Code",
    
    # Standardized Address
    "ELSGenericMessage.StandardizedAddress.STREET1": "Street Address",
    "ELSGenericMessage.StandardizedAddress.STREET2": "Street Address 2",
    "ELSGenericMessage.StandardizedAddress.CITY": "City",
    "ELSGenericMessage.StandardizedAddress.STATE": "State",
    "ELSGenericMessage.StandardizedAddress.ZIP": "ZIP Code",
    "ELSGenericMessage.StandardizedAddress.ZIP4": "ZIP+4",
    
    # Person Information
    "ELSGenericMessage.Stage2Data.Person.FIRSTNAME": "First Name",
    "ELSGenericMessage.Stage2Data.Person.LASTNAME": "Last Name",
    "ELSGenericMessage.Stage2Data.Person.MIDDLENAME": "Middle Name",
    "ELSGenericMessage.Stage2Data.Person.AGE": "Age",
    "ELSGenericMessage.Stage2Data.Person.DATEOFBIRTH": "Date of Birth",
    "ELSGenericMessage.Stage2Data.Person.GENDER": "Gender",
    "ELSGenericMessage.Stage2Data.Person.EDUCATION LEVEL MODEL": "Education Level",
    "ELSGenericMessage.Stage2Data.Person.PERMARITALSTATUS": "Marital Status",
    "ELSGenericMessage.Stage2Data.Person.OCCUPATION": "Occupation",
    "ELSGenericMessage.Stage2Data.Person.INCOME": "Income",
    "ELSGenericMessage.Stage2Data.Person.INCOME_RANGE": "Income Range",
    
    # Living Unit Information
    "ELSGenericMessage.Stage2Data.Livu.ADDR": "Address",
    "ELSGenericMessage.Stage2Data.Livu.RSIZ": "Residence Size",
    "ELSGenericMessage.Stage2Data.Livu.BEDR": "Bedrooms",
    "ELSGenericMessage.Stage2Data.Livu.LIVUCOUNTCHILDREN": "Children in Household",
    "ELSGenericMessage.Stage2Data.Livu.LIVUCOUNTADULTS": "Adults in Household",
    "ELSGenericMessage.Stage2Data.Livu.OWNRENT": "Own/Rent Status",
    "ELSGenericMessage.Stage2Data.Livu.HOMEVALUE": "Home Value",
    "ELSGenericMessage.Stage2Data.Livu.YEARBUILT": "Year Built",
    "ELSGenericMessage.Stage2Data.Livu.SQUAREFEET": "Square Feet",
    
    # Contact Information
    "ELSGenericMessage.Stage2Data.Person.PHONE": "Phone Number",
    "ELSGenericMessage.Stage2Data.Person.EMAIL": "Email Address",
    "ELSGenericMessage.Stage2Data.Person.WIRELESS": "Mobile Number",
    
    # Financial Information
    "ELSGenericMessage.Stage2Data.Person.CREDITCARD": "Credit Card",
    "ELSGenericMessage.Stage2Data.Person.NETWORTH": "Net Worth",
    "ELSGenericMessage.Stage2Data.Person.INVESTMENTVALUE": "Investment Value",
    
    # Lifestyle Information
    "ELSGenericMessage.Stage2Data.Person.INTERESTS": "Interests",
    "ELSGenericMessage.Stage2Data.Person.HOBBIES": "Hobbies",
    "ELSGenericMessage.Stage2Data.Person.LIFESTYLE": "Lifestyle",
}

def map_field_names(data: Any, parent_key: str = "") -> Any:
    """
    Recursively map Experian field names to user-friendly names
    
    Args:
        data: The data structure to transform
        parent_key: The parent key path for building full field paths
        
    Returns:
        Transformed data with user-friendly field names
    """
    if isinstance(data, dict):
        mapped = {}
        for key, value in data.items():
            # Construct the full path key for mapping
            full_key = f"{parent_key}.{key}" if parent_key else key
            
            # Check if we have a mapping for this field
            display_name = FIELD_MAPPINGS.get(full_key, key)
            
            # If no direct mapping found, try to clean up the key name
            if display_name == key and "ELSGenericMessage" in key:
                # Extract the last part after the final dot for unmapped fields
                display_name = key.split(".")[-1].replace("_", " ").title()
            
            # Recursively process nested objects
            mapped_value = map_field_names(value, full_key)
            mapped[display_name] = mapped_value
            
        return mapped
    
    elif isinstance(data, list):
        return [map_field_names(item, parent_key) for item in data]
    
    else:
        return data