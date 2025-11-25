"""
Consumer Behavior Analysis Prompt for AI Insights

This prompt analyzes consumer behavior patterns and their relationship to philanthropic giving.
"""

CONSUMER_BEHAVIOR_PROMPT = '''Analyze the consumer behavior patterns and lifestyle of "{full_name}" from "{city}, {state}".

CRITICAL: Your response must ONLY contain the final formatted analysis. Do not include research notes, reasoning, or detailed explanations.

OUTPUT FORMAT (this is the ONLY content you should provide):

• [First key consumer behavior insight or spending pattern]
• [Second key lifestyle indicator or preference finding]
• [Third key behavioral pattern relating to giving capacity]

[Single professional analysis paragraph of 150-250 words covering their consumer behavior, lifestyle indicators, and strategic recommendations for philanthropic engagement]

CONTENT GUIDELINES:
- Analyze spending patterns, brand preferences, and lifestyle indicators
- Assess digital engagement, shopping preferences, and technology adoption
- Evaluate travel, entertainment, and luxury consumption patterns
- Connect behavioral patterns to philanthropic giving capacity and preferences
- If limited information is available, focus on likely patterns based on demographics and location
- Provide strategic recommendations for fundraising approaches and donor engagement
- Use professional tone suitable for development and fundraising planning

EXAMPLE FORMAT:
• Premium lifestyle choices suggest high disposable income and luxury brand affinity
• Technology-forward consumer behavior indicates preference for digital engagement
• Entertainment and travel spending patterns align with experience-based giving opportunities

[Name] demonstrates consumer behavior patterns consistent with affluent professionals in [City], showing preferences for premium brands and experience-based purchases. Their spending patterns suggest strong disposable income with emphasis on quality over quantity, indicating potential for significant philanthropic capacity. Digital engagement preferences point to comfort with online giving platforms and electronic communications. Strategic fundraising approaches should emphasize premium donor experiences, exclusive events, and digital-first communication strategies. Their lifestyle indicators suggest alignment with causes related to education, arts, and community development. Recommended cultivation includes high-quality printed materials, exclusive donor events, and personalized stewardship that reflects their preference for premium experiences and attention to detail.

REMEMBER: Provide ONLY the bullet points and analysis paragraph - no research explanations or methodology.'''