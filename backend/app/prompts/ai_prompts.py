"""
AI Prompts for Knowledge Core IQ Search

This file imports category-specific prompts for generating AI insights
"""

from .profile_prompt import PROFILE_PROMPT
from .consumer_behavior_prompt import CONSUMER_BEHAVIOR_PROMPT
from .financial_prompt import FINANCIAL_PROMPT
from .political_interests_prompt import POLITICAL_INTERESTS_PROMPT
from .charitable_activities_prompt import CHARITABLE_ACTIVITIES_PROMPT
from .social_media_prompt import SOCIAL_MEDIA_PROMPT
from .news_prompt import NEWS_PROMPT

# Mapping of categories to their prompts
CATEGORY_PROMPTS = {
    'Profile': PROFILE_PROMPT,
    'Consumer Behavior': CONSUMER_BEHAVIOR_PROMPT,
    'Financial': FINANCIAL_PROMPT,
    'Political Interests': POLITICAL_INTERESTS_PROMPT,
    'Charitable Activities': CHARITABLE_ACTIVITIES_PROMPT,
    'Social Media': SOCIAL_MEDIA_PROMPT,
    'News': NEWS_PROMPT
}