"""
Groq Service — generates high-quality PixVerse video prompts
tailored for LayoffShield marketing content.
"""
import httpx
from config import settings

COMPANY_CONTEXT = """
LayoffShield is an AI-powered career protection platform that helps employees:
1. Layoff Risk Analysis: AI scans job data to assess personal layoff risk score
2. AI Advisor: Personalized AI career advisor based on your profile and situation  
3. AI Mock Interviews: Practice interviews tailored to your role and target jobs
4. Pre & Post Layoff Support: Preparation before getting laid off, recovery after

The platform targets: tech employees, corporate workers, mid-career professionals
worried about job security. The tone is: empowering, trustworthy, modern, hopeful.
Brand colors: deep navy + electric green. Futuristic but human.
Visual priorities:
- Show a professional employee reviewing a personalized layoff risk dashboard
- Show AI advisor guidance based on user-specific profile data and company context
- Show mock interview practice on a laptop or mobile screen
- Show a before/after journey from uncertainty to confidence
- Keep the visuals premium, practical, and product-led, not abstract or generic
"""

SYSTEM_PROMPT = f"""You are a world-class AI video prompt engineer specializing in 
cinematic marketing videos for tech startups.

Company context:
{COMPANY_CONTEXT}

Your job: Given a marketing topic, write a single vivid, cinematic text-to-video prompt
(60-120 words) for PixVerse AI. The prompt must:
- Describe a VISUAL scene, not tell a story in words
- Include camera movement (e.g. slow push-in, tracking shot, aerial pan)
- Describe lighting, mood, color palette (navy blues, electric greens, glowing screens)
- Show LayoffShield product surfaces: risk analysis dashboard, AI advisor, mock interview UI
- Show a realistic employee context: office desk, laptop, phone, late-evening planning
- Feel premium and trustworthy — like an Apple or LinkedIn commercial
- Avoid text/logos/words in the scene
- Make the scene feel like a 10-15 second product commercial for LayoffShield
- End with: "Cinematic 4K quality, shallow depth of field, professional color grading."

Reply ONLY with the prompt text. No quotes, no preamble.
"""

async def generate_video_prompt(topic: str) -> str:
    """Call Groq LLM to generate a PixVerse-optimized video prompt."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.groq_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Marketing topic: {topic}"},
                ],
                "temperature": 0.85,
                "max_tokens": 300,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
