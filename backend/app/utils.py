"""
Utility functions for data transformation
"""

from .models import SearchRequest, ExperianPayload

def transform_to_experian_format(search_data: SearchRequest) -> ExperianPayload:
    """
    Transform input data to Experian API format
    
    Args:
        search_data: The validated search request data
        
    Returns:
        ExperianPayload formatted for the API
    """
    return ExperianPayload(
        LEAD_TRANS_DETAILS={
            "FIRST_NAME": search_data.FIRST_NAME,
            "LAST_NAME": search_data.LAST_NAME
        },
        LEAD_ADDRESS={
            "STREET1": search_data.STREET1,
            "STREET2": search_data.STREET2 or "",
            "CITY": search_data.CITY,
            "STATE": search_data.STATE.upper(),
            "ZIP": search_data.ZIP
        }
    )