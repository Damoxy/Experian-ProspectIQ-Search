"""
Social Media Analysis Prompt for AI Insights

This prompt analyzes social media presence and digital engagement patterns.
"""

SOCIAL_MEDIA_PROMPT = '''Analyze the social media presence and digital engagement of "{full_name}" from "{city}, {state}".

CRITICAL: Your response must ONLY contain the final formatted analysis. Do not include research notes, reasoning, or detailed explanations.

OUTPUT FORMAT (this is the ONLY content you should provide):

• [First key social media insight or platform presence finding]
• [Second key digital engagement or networking insight]
• [Third key online reputation or influence element]

[Single professional analysis paragraph of 150-250 words covering their social media presence, digital engagement patterns, and strategic recommendations for online outreach]

CONTENT GUIDELINES:
- Evaluate presence across major platforms (LinkedIn, Facebook, Twitter, Instagram)
- Assess professional networking and digital influence patterns
- Analyze content sharing, engagement levels, and online brand presence
- Consider digital reputation and social connections
- If limited social media presence is found, focus on opportunities for digital engagement
- Provide strategic recommendations for social media outreach and digital communication
- Use professional tone suitable for digital marketing and engagement planning

EXAMPLE FORMAT:
• Active LinkedIn presence with strong professional networking engagement
• Limited personal social media footprint suggesting preference for professional platforms
• High potential for thought leadership content and industry engagement

[Name] maintains a professionally-focused digital presence, primarily active on LinkedIn with limited engagement on personal social platforms. Their social media activity suggests a preference for business networking and professional content over personal sharing. This focused approach indicates strong potential for B2B engagement and professional relationship building. Strategic digital outreach should emphasize LinkedIn connections, industry-relevant content sharing, and professional networking opportunities. Their measured social media approach suggests they would respond well to thoughtful, professional digital communications rather than casual social media engagement. Recommendations include targeted LinkedIn messaging, professional event invitations, and industry-specific content that aligns with their demonstrated interests and professional focus.

REMEMBER: Provide ONLY the bullet points and analysis paragraph - no research explanations or scenarios.'''