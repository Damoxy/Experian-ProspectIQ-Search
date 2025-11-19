"""
Data processing utilities for Experian API responses
"""

import logging
from typing import Any

logger = logging.getLogger('experian_api.data_processing')

def clean_response_data(data: Any) -> Any:
    """
    Recursively clean response data by removing empty, null, or blank values.
    Only returns fields that contain actual data.
    
    Args:
        data: The data structure to clean
        
    Returns:
        Cleaned data structure with empty values removed
    """
    logger.debug(f"Cleaning data of type: {type(data)}")
    
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            cleaned_value = clean_response_data(value)
            if cleaned_value is not None and cleaned_value != "" and cleaned_value != {}:
                cleaned[key] = cleaned_value
        return cleaned if cleaned else None
    
    elif isinstance(data, list):
        cleaned = [clean_response_data(item) for item in data]
        cleaned = [item for item in cleaned if item is not None and item != "" and item != {}]
        return cleaned if cleaned else None
    
    elif isinstance(data, str):
        return data.strip() if data.strip() else None
    
    else:
        return data if data is not None else None