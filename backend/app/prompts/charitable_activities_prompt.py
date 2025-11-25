"""
Charitable Activities Analysis Prompt for AI Insights

This prompt analyzes existing charitable giving patterns and philanthropic engagement.
"""

CHARITABLE_ACTIVITIES_PROMPT = '''Analyze the charitable giving history and philanthropic engagement of "{full_name}" from "{city}, {state}".

CRITICAL: Your response must ONLY contain the final formatted analysis. Do not include research notes, reasoning, or detailed explanations.

OUTPUT FORMAT (this is the ONLY content you should provide):

• [First key giving pattern or charitable sector preference]
• [Second key philanthropic engagement or volunteer involvement finding]
• [Third key charitable activity indicating major gift potential]

[Single professional analysis paragraph of 150-250 words covering their charitable history, giving patterns, and strategic recommendations for major gift cultivation]

CONTENT GUIDELINES:
- Assess historical giving patterns, preferred charitable sectors, and donation amounts
- Evaluate volunteer activities, board service, and fundraising event participation
- Analyze grant-making involvement and recognition for philanthropic activities
- Identify cause preferences and organizational relationship patterns
- If limited charitable data is available, focus on likely interests based on profile and location
- Provide strategic recommendations for cultivation approaches and solicitation timing
- Use professional tone suitable for major gift officers and development professionals

EXAMPLE FORMAT:
• Consistent annual giving history with preference for education and healthcare causes
• Active volunteer leadership demonstrates hands-on philanthropic engagement style
• Board service pattern indicates capacity for significant multi-year commitments

[Name] demonstrates a thoughtful approach to philanthropy with consistent annual giving patterns favoring education and healthcare organizations in the [City] area. Their volunteer leadership roles indicate preference for hands-on engagement rather than passive giving, suggesting they value personal involvement in supported causes. Board service history shows capacity for significant multi-year commitments and strategic thinking about organizational development. Cultivation strategy should emphasize behind-the-scenes briefings, leadership volunteer opportunities, and involvement in strategic planning processes. Their giving pattern suggests readiness for major gift discussions in the $50,000-$250,000 range, particularly for capital campaigns or endowment initiatives. Recommended approach includes peer-to-peer solicitation, exclusive donor events, and opportunities to mentor other philanthropists within their preferred cause areas.

REMEMBER: Provide ONLY the bullet points and analysis paragraph - no fundraising speculation or donor research methodology.'''