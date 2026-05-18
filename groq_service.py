"""
Groq Service — generates high-quality PixVerse video prompts
tailored for LayoffShield marketing content.

Enforces all LayoffShield compliance guidelines including:
- NOT an insurance company (strict enforcement)
- Forbidden terminology filtering
- Approved brand messaging only
- Compliance validation before prompt is returned
- Real-world layoff context integration for meaningful videos
"""
import httpx
import logging
import asyncio
from config import settings
from layoffshield_guidelines import (
    GROQ_SYSTEM_PROMPT_WITH_GUIDELINES,
    validate_video_content,
    APPROVED_VIDEO_THEMES,
)
from layoff_news_fetcher import get_layoff_context_for_video, generate_contextual_prompt_injection

logger = logging.getLogger(__name__)

COMPANY_CONTEXT = """
LayoffShield is an AI-powered career protection platform (NOT an insurance company) based on:
LEGAL FOUNDATION: Tuli & Co Business Model Review (April 2026) - LayoffShield does NOT carry on 
insurance business ONLY IF operated strictly as designed.

SUBSCRIPTION-BASED MODEL:
- Members pay monthly or annual subscription fees (no insurance premium structure)
- Access to core platform: AI risk assessment, career advisor, interview prep, skill analysis, community

CORE SERVICES (Primary Value Proposition):
1. Employment Risk Monitoring: AI analyzes job market data to assess personal layoff risk
   - Real-time industry trends and layoff pattern analytics
   - Personalized risk scoring based on role, company, industry
2. AI Career Advisor: 24/7 personalized guidance on career strategy and preparation
3. AI Mock Interview Practice: Tailored interview prep with instant AI feedback
4. Skill Gap Analysis: Identifies growth areas and career development paths
5. Community Support: Connect with professionals navigating similar career journeys
6. Resume Optimization & Interview Coaching: Tools to enhance career readiness

DISCRETIONARY SUPPORT (Secondary, NOT Insurance):
- May provide voluntary financial support to members facing job loss (at company sole discretion)
- NOT contractually guaranteed, NOT insurance-like, subject to individual case-by-case review
- Terms state: "No Member has any legal or equitable right to receive any support"
- Decision framework is informal with no fixed criteria or formula
- Support availability depends on member engagement, company reserves, individual circumstances

REVENUE MODEL & FUND ALLOCATION:
- Primary Revenue: Subscription fees (monthly/annual)
- Fund Allocation: Minimum 50% to technology infrastructure + platform development
- Remaining: Allocated to "Discretionary Support & Community Reserve" (not ring-fenced, not actuarial)
- NO insurance-style fund structure, underwriting, or risk pooling

EMBEDDED INSURANCE (Premium Tiers - OPTIONAL):
- Optional job loss insurance from licensed insurance companies (NOT from LayoffShield)
- Separate offering with partner branding prominently displayed
- Members can CHOOSE to add optional insurance as supplement to membership
- Insurance terms and disclaimers apply separately

TARGET AUDIENCE:
- Tech industry professionals, corporate workers, mid-career professionals
- Ages 25-50, employed, concerned about career resilience
- Reason for use: Want to understand their employment risk + prepare for career changes

BRAND POSITIONING:
- Career Intelligence Platform + Professional Community
- NOT: Insurance, financial services, income replacement, job guarantee
- Tone: Empowering ("know where you stand"), trustworthy, modern, hopeful
- NOT fear-based; addresses real concerns with data-driven solutions

VISUAL IDENTITY:
- Colors: Deep Navy #0f172a (professional trust) + Electric Green #22c55e (positive energy)
- Style: Premium, tech-forward, bright professional environments
- Hero moments: Risk dashboards, AI recommendations, career growth tools
- Emotional arc: Concern → Clarity → Empowerment (via AI insights)

KEY COMPLIANCE REQUIREMENTS:
✓ NEVER position as insurance company
✓ Use only approved terminology (membership, discretionary support, etc.)
✓ Frame support as voluntary, not guaranteed
✓ Keep core services as star of messaging
✓ Show realistic employee concerns if used as setup (not the focus)
✓ Transform worry into clarity/action via data insights
✓ Maintain professional, empowering tone throughout
"""



async def generate_video_prompt(topic: str, theme: str = None, validate: bool = True, include_realworld_context: bool = True) -> dict:
    """
    Call Groq LLM to generate a PixVerse-optimized video prompt.
    
    Args:
        topic: Marketing topic/focus for the video
        theme: Optional approved theme from APPROVED_VIDEO_THEMES (e.g., 'risk_assessment', 'ai_advisor')
        validate: Whether to validate compliance before returning (default: True)
        include_realworld_context: Include real-world layoff trends for meaningful videos (default: True)
    
    Returns:
        {
            "prompt": str - the generated video prompt,
            "topic": str - the topic used,
            "theme": str - the theme if specified,
            "compliant": bool - whether it passed validation,
            "validation": dict - validation results with violations/warnings,
            "real_world_context_included": bool - whether real-world context was used,
        }
    """
    
    # Build theme context if provided
    theme_context = ""
    if theme and theme in APPROVED_VIDEO_THEMES:
        theme_data = APPROVED_VIDEO_THEMES[theme]
        theme_context = f"""
Specific Theme: {theme_data['theme']}
Approved Messaging: {', '.join(theme_data['messaging'][:2])}
Visual Journey: {' → '.join(theme_data.get('journey', [])[:3] if 'journey' in theme_data else [])}
"""
    
    # Fetch real-world layoff context for more meaningful videos
    real_world_context = ""
    include_context = False
    
    if include_realworld_context:
        try:
            real_world_context = await get_layoff_context_for_video()
            include_context = True
        except Exception as e:
            logger.warning(f"Could not fetch real-world context: {e}")
            include_context = False
    
    # Build the user prompt
    user_prompt = f"""Marketing topic: {topic}
{theme_context if theme_context else ''}

Generate a DETAILED, SPECIFIC cinematic video prompt (400-500 words) for PixVerse that:
1. Shows REAL employee scenario with actual concern (not just sitting in office)
2. Includes SPECIFIC LayoffShield features and dashboards showing real product
3. Shows actual product solving real problems (risk assessment, AI advisor, mock interviews)
4. Transformation arc from real concern to empowerment
5. SPECIFIC scene descriptions with timing, visuals, camera work
6. Vivid colors, cinematic 4K quality, professional atmosphere
7. Ends with empowered professional taking action

Ensure compliance with all guidelines - no forbidden terminology, no insurance language, no false promises.
{f'IMPORTANT: Include awareness of REAL 2024-2025 industry layoff trends, specific affected roles, and how LayoffShield helps navigate actual market challenges.' if include_context else ''}"""
    
    try:
        # Build system prompt with real-world context if available
        system_prompt = GROQ_SYSTEM_PROMPT_WITH_GUIDELINES
        if include_context and real_world_context:
            system_prompt = system_prompt + f"\n\nCURRENT CONTEXT - REAL-WORLD SITUATION:\n{real_world_context}"
        
        async with httpx.AsyncClient(timeout=30) as client:
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                try:
                    response = await client.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.groq_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt},
                            ],
                            "temperature": 0.75,  # Balanced for creativity + compliance
                            "max_tokens": 1200,  # Increased for detailed 400-500 word prompts
                        },
                    )
                    
                    # Handle rate limiting
                    if response.status_code == 429:
                        if attempt < max_retries - 1:
                            wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                            logger.warning(f"Rate limited by Groq. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            raise Exception(f"Rate limited by Groq after {max_retries} retries")
                    
                    response.raise_for_status()
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise  # Last attempt failed, raise the error
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    await asyncio.sleep(retry_delay * (2 ** attempt))
            
            data = response.json()
            generated_prompt = data["choices"][0]["message"]["content"].strip()
            
            # Validate compliance
            validation_result = None
            is_compliant = True
            
            if validate:
                validation_result = validate_video_content(generated_prompt, check_type="strict")
                is_compliant = validation_result["compliant"]
                
                if not is_compliant:
                    logger.warning(f"Compliance violations detected: {validation_result['violations']}")
                else:
                    logger.info(f"✓ Generated prompt passed compliance validation")
            
            return {
                "prompt": generated_prompt,
                "topic": topic,
                "theme": theme,
                "compliant": is_compliant,
                "validation": validation_result,
                "real_world_context_included": include_context,
            }
            
    except Exception as e:
        logger.error(f"Error generating video prompt: {e}")
        raise


async def generate_video_prompt_batch(topics: list[dict], validate: bool = True) -> list[dict]:
    """
    Generate multiple video prompts in sequence.
    
    Args:
        topics: List of dicts with 'topic' and optional 'theme'
        validate: Whether to validate compliance
    
    Returns:
        List of prompt results
    """
    results = []
    for item in topics:
        topic = item.get("topic")
        theme = item.get("theme")
        result = await generate_video_prompt(topic, theme, validate)
        results.append(result)
    return results
