"""
Field mappings for Experian API response transformation
"""

from typing import Any

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
            
            # Extract the last suffix after the final dot
            if "ELSGenericMessage" in full_key and "." in full_key:
                # Get everything after the last dot
                display_name = full_key.split(".")[-1]
                # Clean up underscores and make it more readable
                display_name = display_name.replace("_", " ")
            else:
                # For non-ELS fields, use the key as is
                display_name = key
            
            # Recursively process nested objects
            mapped_value = map_field_names(value, full_key)
            mapped[display_name] = mapped_value
            
        return mapped
    
    elif isinstance(data, list):
        return [map_field_names(item, parent_key) for item in data]
    
    else:
        return data