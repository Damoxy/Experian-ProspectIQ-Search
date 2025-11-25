"""
Political Interests Analysis Prompt for AI Insights

This prompt analyzes political affiliations and civic engagement patterns.
"""

POLITICAL_INTERESTS_PROMPT = '''Analyze the political engagement and civic involvement of "{full_name}" from "{city}, {state}".

CRITICAL: Your response must ONLY contain the final formatted analysis. Do not include research notes, reasoning, or detailed explanations.

OUTPUT FORMAT (this is the ONLY content you should provide):

• [First key political engagement or civic involvement insight]
• [Second key ideological indicator or cause alignment finding]
• [Third key political pattern relating to philanthropic potential]

[Single professional analysis paragraph of 150-250 words covering their political interests, civic engagement, and strategic recommendations for cause-aligned fundraising]

CONTENT GUIDELINES:
- Evaluate voting patterns, party affiliations, and political participation levels
- Assess campaign contributions, advocacy involvement, and issue positions
- Analyze civic organization memberships and community leadership roles
- Connect political interests to potential philanthropic cause alignments
- If limited political data is available, focus on likely engagement based on demographics and location
- Provide strategic recommendations for values-based fundraising approaches
- Use professional tone suitable for political fundraising and cause-based development

EXAMPLE FORMAT:
• Moderate political engagement with focus on local community issues over partisan politics
• Civic involvement suggests alignment with education and infrastructure causes
• Voting patterns indicate support for pragmatic, bipartisan solutions and community development

[Name] demonstrates thoughtful political engagement focused primarily on local community issues rather than partisan politics. Their civic involvement patterns suggest strong alignment with education, infrastructure, and economic development causes that benefit the broader [City] community. Political contribution patterns indicate preference for pragmatic, results-oriented candidates and initiatives over ideological positions. Strategic fundraising approaches should emphasize nonpartisan community impact, measurable outcomes, and collaborative solutions. Their political engagement style suggests they would respond well to fact-based presentations, community leadership involvement, and causes that unite rather than divide. Recommended cultivation includes policy briefings, community impact tours, and opportunities to engage with like-minded civic leaders on shared priorities.

REMEMBER: Provide ONLY the bullet points and analysis paragraph - no political speculation or partisan analysis.'''