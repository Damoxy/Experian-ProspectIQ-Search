"""
AI Insights Service using OpenRouter API

This service generates AI-powered insights for donor profiles using the Google Gemini 2.0 Flash model
through the OpenRouter API.
"""

import json
import httpx
from typing import Dict, Any
from fastapi import HTTPException

from config import DEBUG, OPENROUTER_API_KEY, OPENROUTER_MODEL
from core.logging_config import setup_logging, log_error
from prompts.ai_prompts import CATEGORY_PROMPTS


class AIInsightsService:
    """Service for generating AI insights using OpenRouter API"""
    
    def __init__(self):
        self.logger = setup_logging(DEBUG)
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL
        self.timeout = httpx.Timeout(60.0)  # 60 second timeout for AI generation
        
        # Debug logging for API key
        if not self.api_key:
            self.logger.error("OPENROUTER_API_KEY environment variable not set or is empty")
            raise ValueError("OpenRouter API Key not configured")
        else:
            # Log partial key for debugging (first 10 chars)
            key_preview = f"{self.api_key[:10]}..." if len(self.api_key) > 10 else "KEY_TOO_SHORT"
            self.logger.info(f"OpenRouter API key loaded: {key_preview}")
            self.logger.info(f"Using model: {self.model}")
    
    def _extract_name_and_location(self, profile_data: Dict[str, Any]) -> tuple:
        """
        Extract full name, city, and state from profile data
        
        Args:
            profile_data: The donor profile data
            
        Returns:
            Tuple of (full_name, city, state)
        """
        # Try to extract name components
        first_name = ""
        last_name = ""
        city = ""
        state = ""
        
        # Look for name fields in various formats
        for key, value in profile_data.items():
            key_lower = key.lower()
            if 'first' in key_lower and 'name' in key_lower:
                first_name = str(value) if value else ""
            elif 'last' in key_lower and 'name' in key_lower:
                last_name = str(value) if value else ""
            elif key_lower in ['city', 'town', 'recity']:
                city = str(value) if value else ""
            elif key_lower in ['state', 'region', 'restate']:
                state = str(value) if value else ""
        
        # Construct full name
        full_name = f"{first_name} {last_name}".strip()
        if not full_name:
            full_name = "the individual"
        
        # Use fallback values if location not found
        if not city:
            city = "Unknown City"
        if not state:
            state = "Unknown State"
            
        return full_name, city, state
    
    def _build_prompt(self, category: str, profile_data: Dict[str, Any]) -> str:
        """
        Build the AI prompt based on category and profile data using predefined prompts
        
        Args:
            category: The category for insights (Profile, Financial, etc.)
            profile_data: The donor profile data
            
        Returns:
            Formatted prompt for the AI model
        """
        # Extract name and location
        full_name, city, state = self._extract_name_and_location(profile_data)
        
        # Get the appropriate prompt template
        prompt_template = CATEGORY_PROMPTS.get(category)
        
        if not prompt_template:
            # Fallback to generic prompt if category not found
            return f"Provide professional insights about {full_name} of {city}, {state} for the {category} category based on available information."
        
        # Format the prompt with the extracted information
        formatted_prompt = prompt_template.format(
            full_name=full_name,
            city=city,
            state=state
        )
        
        return formatted_prompt
    
    async def generate_insights(self, category: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI insights for a donor profile category
        
        Args:
            category: The category for insights
            profile_data: The donor profile data
            
        Returns:
            AI-generated insights
            
        Raises:
            HTTPException: If API call fails
        """
        try:
            # Build the prompt
            prompt = self._build_prompt(category, profile_data)
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://knowledgecore-iq-search.com",  # Optional: your site URL
                "X-Title": "Knowledge Core IQ Search"  # Optional: app name
            }
            
            # Make API call
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    error_detail = f"OpenRouter API returned status {response.status_code}"
                    try:
                        error_response = response.json()
                        error_detail = error_response.get('error', {}).get('message', error_detail)
                    except:
                        error_detail = response.text or error_detail
                    
                    self.logger.error(f"AI insights API failed: {error_detail}")
                    raise HTTPException(status_code=response.status_code, detail=error_detail)
                
                # Parse response
                try:
                    api_response = response.json()
                except json.JSONDecodeError as e:
                    error_msg = f"Failed to parse AI insights API response: {str(e)}"
                    log_error(self.logger, error_msg, e)
                    raise HTTPException(status_code=500, detail=error_msg)
                
                # Extract the generated insights
                insights_text = ""
                if "choices" in api_response and len(api_response["choices"]) > 0:
                    insights_text = api_response["choices"][0]["message"]["content"]
                
                formatted_response = {
                    "ai_insights": {
                        "category": category,
                        "insights": insights_text,
                        "model_used": self.model,
                        "tokens_used": api_response.get("usage", {}).get("total_tokens", 0),
                        "generation_status": "success"
                    }
                }
                
                return formatted_response
                
        except HTTPException as he:
            # Return a structured error response
            self.logger.warning(f"AI insights generation failed: {he.detail}")
            
            return {
                "ai_insights": {
                    "category": category,
                    "insights": f"AI insights temporarily unavailable: {he.detail}",
                    "model_used": self.model,
                    "tokens_used": 0,
                    "generation_status": "error",
                    "error": str(he.detail)
                }
            }
        except Exception as e:
            error_msg = f"AI insights generation failed: {str(e)}"
            log_error(self.logger, error_msg, e)
            
            return {
                "ai_insights": {
                    "category": category,
                    "insights": f"AI insights temporarily unavailable due to technical issues.",
                    "model_used": self.model,
                    "tokens_used": 0,
                    "generation_status": "error",
                    "error": str(e)
                }
            }