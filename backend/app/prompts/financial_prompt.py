"""
Financial Analysis Prompt for AI Insights

This prompt analyzes financial capacity and giving potential based on available data.
"""

FINANCIAL_PROMPT = '''Analyze the financial capacity and wealth indicators of "{full_name}" from "{city}, {state}".

CRITICAL: Your response must ONLY contain the final formatted analysis. Do not include research notes, reasoning, or detailed explanations.

OUTPUT FORMAT (this is the ONLY content you should provide):

• [First key financial capacity indicator or wealth marker]
• [Second key asset or investment insight]
• [Third key giving capacity or solicitation recommendation]

[Single professional analysis paragraph of 150-250 words covering their financial profile, giving capacity, and strategic recommendations for major gift solicitation]

CONTENT GUIDELINES:
- Assess income indicators, wealth markers, and asset ownership patterns
- Evaluate property holdings, investment sophistication, and business ownership
- Analyze credit indicators and financial responsibility markers
- Compare wealth position relative to geographic region
- If limited financial data is available, focus on likely capacity based on profession and location
- Provide strategic recommendations for gift solicitation approaches and timing
- Use professional tone suitable for major gift officers and development planning

EXAMPLE FORMAT:
• Property ownership and location suggest significant real estate wealth accumulation
• Professional background indicates high earning potential and investment sophistication
• Geographic wealth indicators support major gift capacity in $25,000-$100,000 range

[Name] demonstrates strong financial capacity consistent with successful professionals in [City], with wealth indicators suggesting significant philanthropic potential. Property ownership and location data indicate substantial real estate assets and investment acumen. Professional background and regional wealth comparisons support major gift capacity in the $25,000-$100,000 annual giving range. Optimal solicitation timing should align with fiscal year-end tax planning considerations and quarterly business cycles. Recommended approach includes cultivation through exclusive briefings, major gift proposals emphasizing tax benefits, and multi-year pledge options to accommodate cash flow preferences. Estate planning discussions may reveal planned giving opportunities, particularly given their demonstrated wealth accumulation and investment sophistication.

REMEMBER: Provide ONLY the bullet points and analysis paragraph - no research process or detailed calculations.'''