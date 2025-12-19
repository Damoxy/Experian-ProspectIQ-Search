"""
Profile Biography Prompt for AI Insights

This prompt generates professional biographies for individuals based on their name and location.
"""

PROFILE_PROMPT = '''Create a professional biography for "{full_name}" of "{city}, {state}".

CRITICAL INSTRUCTION: Your final output must ONLY contain the bulleted highlights and the final biography paragraph. Do NOT include any of your research, reasoning, or preliminary notes in the response.

RESEARCH PROCESS (for your reference, do not include in output):
- Gather relevant, accurate information about the subject's education, business affiliations, career highlights, professional achievements, professional licensures, bar admissions, and community involvement.
- Synthesize the facts and qualifications found into a cohesive biography.
- If current information is incomplete or unavailable, create a realistic professional profile based on their location and likely career paths.

OUTPUT FORMAT (This is the ONLY content you should provide):
• [First key achievement/credential]
• [Second key achievement/credential] 
• [Third key achievement/credential]

[Single professional paragraph of 150-250 words describing their background, education, career, and contributions in a professional, third-person tone.]

REMEMBER: Provide ONLY the bullet points and the final paragraph. No reasoning, no notes, no "Here is the biography" introductory text. Just the final, clean output.
'''