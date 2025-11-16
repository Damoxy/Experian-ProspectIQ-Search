"""
Value mappings for Experian API response codes to human-readable descriptions
"""

from typing import Dict, Any, Optional

# Value mappings for converting API response codes to readable descriptions
VALUE_MAPPINGS: Dict[str, Dict[str, str]] = {
    # Education Level mappings
    "EDUCATION_LEVEL": {
        "00": "Unknown",
        "11": "HS Diploma - Extremely Likely",
        "12": "Some College - Extremely Likely",
        "13": "Bach Degree - Extremely Likely",
        "14": "Grad Degree - Extremely Likely",
        "15": "Less than HS Diploma - Extremely Likely",
        "51": "HS Diploma - Likely",
        "52": "Some College - Likely",
        "53": "Bach Degree - Likely",
        "54": "Grad Degree - Likely",
        "55": "Less than HS Diploma - Likely",
        "": "Null",
        " ": "Null"
    },
    
    # Marital Status mappings
    "MARITAL_STATUS": {
        "0U": "Unknown Not scored",
        "1M": "Married Extremely Likely",
        "5M": "Married Likely",
        "5S": "Single Likely never married",
        "5U": "Unknown Scored",
        "": "Null",
        " ": "Null"
    },
    
    # Add more field mappings here as needed
    # Template for new mappings:
    # "FIELD_NAME": {
    #     "code1": "Description 1",
    #     "code2": "Description 2",
    #     "": "Null",
    #     " ": "Null"
    # },
}

# Field name to mapping key lookup (using mapped field names)
FIELD_TO_MAPPING_KEY: Dict[str, str] = {
    "Level of Education": "EDUCATION_LEVEL",     # Mapped from "EDUCATION LEVEL MODEL"
    "Marital Status": "MARITAL_STATUS",          # Mapped from "PERMARITALSTATUS"
}

def map_field_values(data: Any, field_name: str = "") -> Any:
    """
    Convert API response codes to human-readable descriptions
    
    Args:
        data: The value to transform
        field_name: The field name to determine which mapping to use
        
    Returns:
        Transformed value with human-readable description
    """
    if not isinstance(data, (str, int)):
        return data
    
    # Convert to string for mapping lookup
    value_str = str(data).strip()
    
    # Find the mapping key for this field
    mapping_key = FIELD_TO_MAPPING_KEY.get(field_name)
    if not mapping_key:
        # Debug: Print unmapped field names
        print(f"DEBUG: No mapping key found for field: '{field_name}'")
        return data
    
    # Get the mapping dictionary
    mapping_dict = VALUE_MAPPINGS.get(mapping_key, {})
    
    # Debug: Print mapping attempts
    print(f"DEBUG: Field '{field_name}' -> Key '{mapping_key}' -> Value '{value_str}'")
    
    # Return mapped value or original if no mapping found
    mapped_value = mapping_dict.get(value_str, data)
    if mapped_value != data:
        print(f"DEBUG: Mapped '{value_str}' to '{mapped_value}'")
    else:
        print(f"DEBUG: No mapping found for value '{value_str}' in '{mapping_key}'")
    
    return mapped_value

def transform_response_data(data: Any, parent_field: str = "") -> Any:
    """
    Recursively transform response data by mapping both field names and values
    
    Args:
        data: The data structure to transform
        parent_field: The parent field name for context
        
    Returns:
        Fully transformed data with mapped field names and values
    """
    if isinstance(data, dict):
        transformed = {}
        for key, value in data.items():
            # First, transform nested objects
            if isinstance(value, (dict, list)):
                transformed_value = transform_response_data(value, key)
            else:
                # Map the field value using the field name as context
                transformed_value = map_field_values(value, key)
            
            transformed[key] = transformed_value
            
        return transformed
    
    elif isinstance(data, list):
        return [transform_response_data(item, parent_field) for item in data]
    
    else:
        # For leaf values, try to map using parent field context
        return map_field_values(data, parent_field)

def add_value_mapping(field_name: str, mapping_key: str, mappings: Dict[str, str]) -> None:
    """
    Add a new value mapping for a field
    
    Args:
        field_name: The display name of the field
        mapping_key: The key to use in VALUE_MAPPINGS dictionary
        mappings: Dictionary of code -> description mappings
    """
    VALUE_MAPPINGS[mapping_key] = mappings
    FIELD_TO_MAPPING_KEY[field_name] = mapping_key

def get_available_mappings() -> Dict[str, list]:
    """
    Get a summary of all available mappings
    
    Returns:
        Dictionary with mapping keys and their available codes
    """
    return {
        key: list(mapping.keys()) 
        for key, mapping in VALUE_MAPPINGS.items()
    }