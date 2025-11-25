"""
News and Media Coverage Analysis Prompt for AI Insights

This prompt analyzes news mentions and media coverage patterns.
"""

NEWS_PROMPT = '''Analyze the news coverage and media presence of "{full_name}" from "{city}, {state}".

CRITICAL: Your response must ONLY contain the final formatted analysis. Do not include research notes, reasoning, assumptions, or scenarios.

OUTPUT FORMAT (this is the ONLY content you should provide):

• [First key media insight or coverage highlight]
• [Second key media insight or public presence finding]
• [Third key media insight or reputation element]

[Single professional analysis paragraph of 150-250 words covering their news presence, media coverage, public recognition, and strategic recommendations for engagement]

CONTENT GUIDELINES:
- Analyze recent news mentions and media coverage patterns
- Assess press releases, public announcements, and industry recognition
- Evaluate speaking engagements, thought leadership, and public visibility
- Consider media sentiment and public perception factors
- If limited media presence is found, focus on potential for media engagement and reputation building
- Provide strategic recommendations for media outreach and public relations
- Use professional tone suitable for PR and communications planning

EXAMPLE FORMAT:
• Limited recent media coverage with potential for increased visibility
• Strong local business presence suggests media-ready professional background
• Opportunity for thought leadership in industry publications and local media

[Name] maintains a relatively low public media profile, with minimal recent news coverage or press mentions. However, their professional background and location in [City] present significant opportunities for increased media visibility and thought leadership. Strategic media engagement could include contributing expert commentary to industry publications, participating in local business forums, and developing a content strategy around their professional expertise. Their position in the [City] market provides natural opportunities for local media relationships and community-focused publicity. A proactive media strategy focusing on industry expertise and community involvement could establish them as a recognized thought leader while maintaining professional credibility.

REMEMBER: Provide ONLY the bullet points and analysis paragraph - no research process, scenarios, or assumptions.'''