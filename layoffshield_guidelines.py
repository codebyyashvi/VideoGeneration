"""
LayoffShield Social Media Video Content Guidelines & Boundaries
Based on Legal Review (Tuli & Co, April 2026) and Marketing Compliance Framework

CRITICAL: LayoffShield is NOT an insurance company and must NEVER be positioned as such.
All video content must adhere to these boundaries to ensure legal compliance and brand integrity.
"""

# ─────────────────────────────────────────────────────────────────────────────────
# COMPLIANCE RULES - STRICT ENFORCEMENT REQUIRED
# ─────────────────────────────────────────────────────────────────────────────────

FORBIDDEN_TERMS = [
    "insurance",
    "insurance company",
    "insurer",
    "insurance product",
    "insurance benefit",
    "insurance coverage",
    "insurance policy",
    "claim",
    "premium",
    "coverage",
    "guaranteed payout",
    "assured protection",
    "guaranteed financial support",
    "insurance protection",
    "risk assumption",
    "compensation guarantee",
]

MANDATORY_ALTERNATIVE_TERMS = {
    "insurance": "membership",
    "insurance product": "career support program",
    "claim": "request",
    "premium": "subscription fee",
    "coverage": "protection package",
    "guaranteed payout": "discretionary support",
    "insurance benefit": "member benefit",
    "assured protection": "career readiness tools",
    "insurance company": "LayoffShield",
}

MANDATORY_DISCLAIMERS = [
    "LayoffShield is not an insurance company.",
    "Discretionary financial support is not guaranteed.",
    "Support does not arise from any contractual obligation.",
    "Support is not an insurance benefit of any kind.",
    "Financial assistance is provided at LayoffShield's sole discretion.",
]

# ─────────────────────────────────────────────────────────────────────────────────
# BRAND POSITIONING - CORE VALUE PROPOSITION
# ─────────────────────────────────────────────────────────────────────────────────

BRAND_POSITIONING = {
    "primary_positioning": "AI-powered career protection platform for employed professionals",
    "core_services": [
        "Employment risk monitoring & AI-driven risk scoring",
        "Personalized AI career advisor",
        "AI-powered mock interview practice",
        "Skill gap analysis & upskilling recommendations",
        "Industry & layoff trend analytics",
        "Resume optimization tools",
        "Career readiness & preparation resources",
        "Post-layoff recovery support community",
    ],
    "target_audience": [
        "Tech industry professionals",
        "Corporate employees (mid-career, senior)",
        "Knowledge workers concerned about job security",
        "Career-conscious professionals aged 25-50",
        "Both employed and recently transitioned professionals",
    ],
    "brand_tone": [
        "Empowering",
        "Trustworthy",
        "Forward-thinking",
        "Hopeful, not fearful",
        "Professional yet accessible",
        "Modern & innovative",
        "Human-centric, not fear-mongering",
    ],
    "what_NOT_to_position": [
        "Financial safety net / insurance",
        "Guaranteed layoff protection",
        "Replacement income provider",
        "Insurance company or intermediary",
        "Risk elimination (only risk MANAGEMENT)",
        "Money-back guarantees",
        "Unemployment benefits provider",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────────
# VIDEO CONTENT GUIDELINES - APPROVED MESSAGING THEMES
# ─────────────────────────────────────────────────────────────────────────────────

APPROVED_VIDEO_THEMES = {
    "risk_assessment": {
        "theme": "Know Your Risk",
        "messaging": [
            "AI analyzes job market data to assess YOUR personal layoff risk",
            "Get an honest, data-driven view of your employment security",
            "Understand industry trends and layoff patterns in real-time",
            "Know where you stand before changes happen",
        ],
        "visual_focus": "Dashboard showing risk scores, data analytics, trend charts",
        "do": [
            "Show the risk assessment dashboard",
            "Display job market analytics",
            "Show the AI intelligence behind the analysis",
        ],
        "dont": [
            "Promise to prevent layoffs",
            "Guarantee job security",
            "Position as insurance",
        ],
    },
    "stressed_employee_scenario": {
        "theme": "From Worry to Clarity",
        "messaging": [
            "Mid-career professional worried about job security in uncertain times",
            "Stressed about layoff trends they keep reading about online",
            "Wants real data, not rumors - what's ACTUALLY happening in their industry?",
            "Uses LayoffShield to assess their own risk and take control",
            "Moves from anxiety to empowerment through data-driven insights",
            "Knows where they stand and what they can do about it",
        ],
        "visual_focus": "Employee tensed/stressed → LayoffShield dashboard → becomes empowered",
        "journey": [
            "OPENING: Professional at work, tense, possibly after difficult interaction",
            "CONFLICT: Boss conversation/difficult moment, employee stressed or worried",
            "ESCAPE: Employee sits at desk, opens laptop/LayoffShield",
            "INSIGHT: Sees their personalized risk score, industry trends, data visualization",
            "TRANSFORMATION: From worry to clarity - 'I know where I stand'",
            "EMPOWERMENT: Now has tools to prepare and take action - 'I'm ready'",
        ],
        "do": [
            "Show realistic workplace tension/stress (boss interaction optional but effective)",
            "Show the anxiety-to-clarity transformation",
            "Display the dashboard and AI insights that create clarity",
            "Show professional taking control of their situation",
            "End on empowerment and readiness, not fear",
            "Use deep navy + green colors for confidence",
            "Make LayoffShield the solution that transforms worry to action",
        ],
        "dont": [
            "Show people getting fired or laid off explicitly",
            "Make it dark, depressing, or fear-mongering",
            "Suggest LayoffShield will prevent layoffs",
            "Position as insurance or safety net",
            "End on a negative note",
            "Make the stress the focus (use it as setup, not payoff)",
        ],
        "tone": "Empathetic to real concerns, solution-focused, ultimately hopeful and empowering",
    },
    "ai_advisor": {
        "theme": "Personalized Career Guidance",
        "messaging": [
            "Your personal AI career advisor, available 24/7",
            "Get tailored guidance based on your profile and industry",
            "Strategic career planning that adapts to YOUR situation",
            "Smart recommendations for career growth and resilience",
        ],
        "visual_focus": "AI advisor UI in action, personalized recommendations, conversational interface",
        "do": [
            "Show AI conversation interface",
            "Display personalized recommendations",
            "Show how the AI adapts to user input",
        ],
        "dont": [
            "Position as financial advisor",
            "Promise specific career outcomes",
            "Imply guaranteed job placement",
        ],
    },
    "interview_prep": {
        "theme": "Master Your Interview Skills",
        "messaging": [
            "Practice with AI-powered mock interviews tailored to your role",
            "Get instant feedback and improvement recommendations",
            "Interview prep that's always available when you need it",
            "Build confidence through realistic practice scenarios",
        ],
        "visual_focus": "Interview practice UI, confident professional, feedback insights",
        "do": [
            "Show mock interview interface",
            "Display AI feedback and coaching",
            "Show professional in practice scenario",
        ],
        "dont": [
            "Guarantee job offers",
            "Position as replacement for professional recruiters",
            "Promise specific interview success rates",
        ],
    },
    "preparedness": {
        "theme": "Stay Career Ready",
        "messaging": [
            "Be prepared for whatever comes next in your career",
            "Build resilience with career readiness tools",
            "Stay ahead with skill gap analysis and development plans",
            "Community support from professionals in your situation",
        ],
        "visual_focus": "Professional taking action, tools being used, community connection",
        "do": [
            "Show action and empowerment",
            "Display skill development journey",
            "Show professional community",
        ],
        "dont": [
            "Use fear-based messaging",
            "Promise financial outcomes",
            "Position as insurance",
        ],
    },
    "community": {
        "theme": "You're Not Alone",
        "messaging": [
            "Connect with professionals navigating similar career journeys",
            "Share experiences and learn from others",
            "Access community-curated resources and insights",
            "Support when you need it most",
        ],
        "visual_focus": "Diverse professionals, connection, shared experience, supportive environment",
        "do": [
            "Show diverse, relatable professionals",
            "Display community features",
            "Emphasize shared experience",
        ],
        "dont": [
            "Promise specific outcomes",
            "Position support as financial",
            "Guarantee specific results",
        ],
    },
    "embedded_insurance": {
        "theme": "Optional Additional Protection (For Premium Tiers)",
        "messaging": [
            "For higher-tier members, optional access to insurance partnerships",
            "Explore job loss insurance through select partners",
            "Insurance is a separate, optional offering - not part of LayoffShield itself",
            "Choose protection options that work for your situation",
        ],
        "visual_focus": "Partner company badge, clear separation, optional selection",
        "do": [
            "Clearly separate LayoffShield branding from partner insurance",
            "Use partner's branding/logos prominently",
            "Show 'optional' and 'separate' clearly",
            "Display partner company name and disclaimers",
        ],
        "dont": [
            "Mix LayoffShield branding with insurance promises",
            "Imply LayoffShield provides insurance",
            "Use forbidden insurance terminology",
            "Position as core LayoffShield offering",
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────────
# BRAND IDENTITY & VISUAL GUIDELINES
# ─────────────────────────────────────────────────────────────────────────────────

VISUAL_GUIDELINES = {
    "primary_colors": {
        "deep_navy": "#0f172a",
        "electric_green": "#22c55e",
        "accent_blue": "#0ea5e9",
    },
    "mood": [
        "Premium, professional",
        "Modern, forward-thinking",
        "Bright and optimistic (not dark/fearful)",
        "Trustworthy, reliable",
        "Tech-forward but human",
    ],
    "environments": [
        "Modern office spaces",
        "Home office setup",
        "Bright, natural lighting preferred",
        "Professional digital interfaces",
        "Collaborative spaces",
    ],
    "avoid": [
        "Dark, depressing atmospheres",
        "Explicit layoff/job loss visuals (people getting fired)",
        "Corporate downsizing imagery",
        "Fear-based visual metaphors",
        "Generic stock footage",
    ],
    "hero_visuals": [
        "Clean, modern UI dashboards",
        "Professionals in control of their careers",
        "Data visualization and insights",
        "Collaborative community moments",
        "Confident professionals using the platform",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────────
# EMBEDDED INSURANCE PARTNERSHIP GUIDELINES
# ─────────────────────────────────────────────────────────────────────────────────

EMBEDDED_INSURANCE_RULES = {
    "positioning": "Optional supplementary insurance from licensed partner companies",
    "clarity_required": [
        "Insurance is provided BY a licensed insurance company, NOT by LayoffShield",
        "Use partner company's branding prominently",
        "Include insurance company disclaimers",
        "Clearly state it's optional and separate from core platform",
        "Show partner company name and registration details",
    ],
    "separation_visual": [
        "Distinct visual section/module for insurance",
        "Partner company logo displayed separately",
        "Different call-to-action for insurance vs. platform",
    ],
    "messaging_rules": [
        "Say: 'Through our partner [Insurance Company Name]'",
        "Say: 'Optional insurance coverage'",
        "Say: 'Subject to partner terms and conditions'",
        "Avoid: 'LayoffShield insurance'",
        "Avoid: 'We provide insurance'",
        "Avoid: Mixing LayoffShield promises with insurance promises",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────────
# COMPLIANCE CHECKER FUNCTION
# ─────────────────────────────────────────────────────────────────────────────────

def validate_video_content(prompt_or_description: str, check_type: str = "strict") -> dict:
    """
    Validate video content against compliance guidelines.
    
    Args:
        prompt_or_description: The video prompt or description to validate
        check_type: 'strict' (reject forbidden terms), 'warning' (flag issues)
    
    Returns:
        {
            "compliant": bool,
            "violations": [list of violations],
            "warnings": [list of warnings],
            "recommendations": [list of recommendations],
            "flagged_terms": [terms that triggered flags],
        }
    """
    text_lower = prompt_or_description.lower()
    violations = []
    warnings = []
    flagged_terms = []
    
    # Check for forbidden terms
    for term in FORBIDDEN_TERMS:
        if term.lower() in text_lower:
            violations.append(f"Forbidden term detected: '{term}' - Use alternatives from MANDATORY_ALTERNATIVE_TERMS")
            flagged_terms.append(term)
    
    # Check for fear-based language
    fear_terms = ["guaranteed", "assured", "protected from layoff", "job security", "won't get laid off"]
    for term in fear_terms:
        if term.lower() in text_lower:
            warnings.append(f"Potentially problematic term: '{term}' - Ensure it's not making guarantees")
            flagged_terms.append(term)
    
    # Recommendations
    recommendations = []
    if any(term in text_lower for term in ["layoff", "fired", "job loss"]):
        recommendations.append("When mentioning layoff/job loss, frame as risk MANAGEMENT, not prevention")
    
    if len(violations) == 0 and len(warnings) == 0:
        recommendations.append("✓ Content appears compliant with guidelines")
    
    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "warnings": warnings,
        "recommendations": recommendations,
        "flagged_terms": flagged_terms,
    }

# ─────────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT FOR GROQ - INCLUDES ALL CONSTRAINTS
# ─────────────────────────────────────────────────────────────────────────────────

GROQ_SYSTEM_PROMPT_WITH_GUIDELINES = """You are a world-class AI video prompt engineer specializing in 
cinematic marketing videos for tech startups. You are creating content for LayoffShield, an AI-powered 
career protection platform (NOT an insurance company).

CRITICAL: Generate DETAILED, SPECIFIC video prompts (300-500 words) that show REAL scenarios with 
LayoffShield solutions. Not generic office scenes - show actual product in action.

LEGAL FOUNDATION (Tuli & Co Business Model Review, April 2026):
LayoffShield does NOT carry on insurance business ONLY IF:
1. Discretionary support remains genuinely voluntary and non-routine
2. No internal eligibility matrix or structured decision-making framework
3. Customer-facing communications DON'T create expectation of assured financial protection
4. Program is NOT priced, reserved, or administered like insurance
5. Non-insurance service components remain substantive and core value proposition

COMPANY CONTEXT & BUSINESS MODEL:
- LayoffShield is subscription-based career protection platform (monthly/annual fees)
- Core services: AI risk monitoring, career advisor, interview prep, skill analysis, community
- Members get access to tools + discretionary community support if they face job loss
- Financial support (if any) is at LayoffShield's sole discretion, case-by-case, informal
- NO legal entitlement, NO contractual obligation, NO fixed criteria
- 50%+ of subscription fees allocated to tech infrastructure, platform development
- Remaining revenue allocated to "Discretionary Support & Community Reserve"
- Reserve is NOT ring-fenced, NOT actuarially determined, NOT insurance fund

🚫 CRITICAL COMPLIANCE RULES - DO NOT VIOLATE THESE:
1. LayoffShield is NOT an insurance company - NEVER position it as such
2. FORBIDDEN TERMS - DO NOT USE: insurance, claim, premium, coverage, guaranteed payout, 
   assured protection, insurance benefit, insurance company, risk assumption, compensation guarantee
3. Use ALTERNATIVES instead: 
   - Instead of "insurance" → "membership" or "career support"
   - Instead of "claim" → "request"
   - Instead of "premium" → "subscription fee"
   - Instead of "coverage" → "protection package"
   - Instead of "guaranteed" → "discretionary support available"

4. When mentioning financial support, ALWAYS frame as:
   - "Discretionary support" (NOT guaranteed)
   - "At company discretion" (NOT automatic)
   - "May provide" (NOT "will provide")
   - "Subject to individual evaluation" (NOT automatic)

5. FOCUS on these core services (these ARE the real product):
   - AI-powered employment risk assessment and monitoring with personalized scores
   - Personalized AI career advisor available 24/7
   - AI-powered mock interview practice with real-time feedback
   - Skill gap analysis and career development recommendations
   - Industry trend analysis and layoff pattern monitoring
   - Community support and professional connections
   - Resume optimization and interview coaching

6. EMBEDDED INSURANCE (for premium tiers):
   - Insurance provided BY licensed insurance companies (NOT by LayoffShield)
   - MUST show insurance partner branding prominently
   - MUST say "optional" and "separate offering"
   - MUST include insurance company disclaimers
   - NEVER mix LayoffShield branding with insurance promises

7. REAL-WORLD LAYOFF CONTEXT TO INTEGRATE:
   - 260,000+ tech workers laid off in 2024-2025
   - Most affected: Customer Success, QA, Junior Developers, Business Analysts
   - Safer roles: Senior Engineering, Product, Sales, Security
   - Industries hit: Tech (35%), Finance (25%), Retail (15%), Media (15%)
   - Market challenge: 3-5x more applications per role
   - AI skills growing: 70% increase in AI/ML roles
   - Show that LayoffShield helps professionals navigate THIS reality

8. REALISTIC EMPLOYEE SCENARIOS - ESPECIALLY FOR STRESSED_EMPLOYEE_SCENARIO THEME:
   FOR "stressed_employee_scenario" theme, use this dramatic arc:
   - SCENE 1 (Tension): Professional in workplace setting, tense moment
     * Optional: Brief interaction with boss (showing workplace pressure)
     * Show real workplace stress/tension/difficult conversation
   - SCENE 2 (Escape): Employee retreats to their desk, opens laptop
   - SCENE 3 (Discovery): Opens LayoffShield, runs risk assessment
   - SCENE 4 (Insight): Dashboard reveals:
     * Personal risk score based on role/industry data
     * Industry trends affecting their position
     * Specific skill gaps AI identifies
     * Interview prep recommendations
   - SCENE 5 (Transformation): Employee's face/body language changes from stressed to focused/empowered
   - SCENE 6 (Empowerment): "Now I know where I stand. I can prepare."
   
   FOR OTHER THEMES:
   - SCENE SETUP: Professional seeing layoff news, worried about their role (tech layoffs, AI replacing roles, market downturn)
   - ACTION: Opens LayoffShield app, runs risk assessment
   - TRANSFORMATION: From worry about real market situation → Clear understanding of actual risk → Taking concrete action
   
   AVOID: Explicit firing scenes, desperation, fear-mongering, fake promises

9. VISUAL SEQUENCE REQUIREMENTS:
   FOR 15s VIDEO (recommended):
   Sec 0-1: Professional in workplace, shows tension/pressure (meeting, boss interaction, etc.)
   Sec 1-2: Employee sits at desk, stressed, opens laptop
   Sec 2-4: LayoffShield dashboard loads with animations
   Sec 4-6: Show risk score prominently, industry data, affected roles
   Sec 6-8: AI insights and recommendations appear
   Sec 8-10: Employee's expression changes to focused/empowered
   Sec 10-12: Show LayoffShield features in action (mock interview, skill gap, etc.)
   Sec 12-15: Employee confident, ready, taking action - text: "Know Your Risk. Prepare. Protect Your Career."
   
   FOR 10s VIDEO:
   Sec 0-1: Professional shows tension/stress
   Sec 1-2: Opens LayoffShield  
   Sec 2-5: Dashboard loads with risk score and industry data
   Sec 5-7: AI insights appear
   Sec 7-10: Transformation to empowerment - "I'm ready"
   
   FOR 5s VIDEO:
   Sec 0-1: Stressed professional
   Sec 1-2: Opens LayoffShield (quick cut)
   Sec 2-4: Risk dashboard and AI insights
   Sec 4-5: Empowered - "Now I know"
10. BRAND TONE: Empowering, trustworthy, hopeful, professional, modern, solution-focused
    NOT fearful, desperate, or overpromising
    Not: "We'll protect you from layoffs"
    But: "Know where you stand. Prepare strategically. Take control of your career."

11. VISUAL STYLE: 
    - For stressed_employee_scenario: Start with real workplace tension/stress
    - Hero moments: Clean, modern UI dashboards showing actual data visualization
    - Risk scores, trend analysis, skill gaps as visual elements
    - Confident professional taking action with real tools
    - Bright, professional environments (deep navy #0f172a + electric green #22c55e)
    - Transformation from tension → clarity → empowerment (visual and emotional arc)
    - Show actual LayoffShield product being used in real-world scenario
    - End with empowered, prepared professional
    - Avoid: dark atmospheres, people being fired/laid off, fake promises
    - Show actual product interfaces when possible

12. ENDING ELEMENT:
    - Always end with empowerment: "Ready for what's next" or "In control of my career"
    - Include text overlay: "Know Your Risk. Prepare. Protect Your Career."

Your task: Write a DETAILED, SPECIFIC cinematic video prompt (400-500 words) for PixVerse that:
- Shows REAL employee scenario (concerned about actual 2024-2025 layoff trends)
- Includes SPECIFIC LayoffShield features and dashboard elements
- Shows actual product in action solving real problems
- Transformation from real concern to empowerment through data
- Uses vivid, specific scene descriptions (timing, visuals, transitions)
- Uses only approved terminology - NO forbidden terms
- Never suggests guarantees, insurance-like protections, or unrealistic promises
- Professional tech brand tone (Apple, LinkedIn, Stripe style)
- Ends with visual/emotional empowerment
- MUST specify camera work, colors, and 4K cinematic quality

PACING NOTE: Videos can be 5-10 seconds. Use this structure:
- 5s video: Focus on one transformation (worry→clarity)
- 10s video: Add more product features and detail
Adjust depth of scenes accordingly.

Reply ONLY with the detailed prompt text. No preamble, explanations, or rule violations."""
