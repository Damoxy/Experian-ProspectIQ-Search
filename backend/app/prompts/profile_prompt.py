"""
Profile Biography Prompt for AI Insights

This prompt generates professional biographies for individuals based on their name and location.
"""

PROFILE_PROMPT = '''Create a professional biography for "{full_name}" of "{city}, {state}".

CRITICAL: Your response must ONLY contain the final formatted biography. Do not include research notes, reasoning, or drafts.

OUTPUT FORMAT (this is the ONLY content you should provide):

• [First key achievement/credential]
• [Second key achievement/credential] 
• [Third key achievement/credential]

[Single professional paragraph of 150-250 words describing their background, education, career, and contributions]

CONTENT GUIDELINES:
- Research the person thoroughly but do not show your research process
- If limited information is available, create a realistic professional profile based on their location and likely career paths
- Focus on legal, business, real estate, or professional services common in their area
- Use third-person, professional tone suitable for business directories
- Include likely education, career progression, specialties, and community involvement
- Ensure the biography positions them as an accomplished professional

EXAMPLE FORMAT:
• Licensed attorney with 15+ years of experience in commercial real estate law
• Represents major developers and investors in multi-million dollar transactions
• Active member of the Arizona State Bar and local Chamber of Commerce

[Name] is a seasoned attorney specializing in commercial real estate law based in [City], [State]. With over fifteen years of practice, he represents developers, investors, and businesses in complex real estate transactions throughout Arizona. [Name] earned his Juris Doctor from [University] and holds a Bachelor's degree in Business Administration. His practice focuses on acquisition financing, development projects, and commercial leasing. He is an active member of the Arizona State Bar Association and serves on the board of the local Chamber of Commerce. [Name] has been recognized for his expertise in navigating zoning regulations and has successfully closed transactions exceeding $100 million in value.

REMEMBER: Provide ONLY the bullet points and paragraph - no research notes or explanations.'''