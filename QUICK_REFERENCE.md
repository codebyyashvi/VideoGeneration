# LayoffShield Content Creation - QUICK REFERENCE

**TL;DR** - Essential compliance rules for video content creators

---

## ❌ FORBIDDEN TERMS (NEVER USE)

```
insurance          →  Use: "membership" or "career support"
insurance company  →  Use: "LayoffShield"
claim              →  Use: "request"
premium            →  Use: "subscription fee"
coverage           →  Use: "protection package"
guaranteed payout  →  Use: "discretionary support"
assured protection →  Use: "career readiness tools"
```

---

## ✅ APPROVED THEMES (USE THESE)

### 1. Risk Assessment ("Know Your Risk")
- Messaging: Data-driven, insightful, empowering
- Visual: Dashboards, analytics, trend charts
- API: `theme: "risk_assessment"`

### 2. AI Advisor ("Personalized Career Guidance")
- Messaging: Tailored, adaptive, supportive
- Visual: AI interface, recommendations
- API: `theme: "ai_advisor"`

### 3. Interview Prep ("Master Your Interview Skills")
- Messaging: Practice, feedback, confidence
- Visual: Interview interface, feedback insights
- API: `theme: "interview_prep"`

### 4. Career Readiness ("Stay Career Ready")
- Messaging: Proactive, empowering, forward-thinking
- Visual: Professional action, skill development
- API: `theme: "preparedness"`

### 5. Community ("You're Not Alone")
- Messaging: Supportive, inclusive, warm
- Visual: Diverse professionals, connection
- API: `theme: "community"`

### 6. Insurance Partnership (Premium Only - SEPARATA!)
- **MUST show partner insurance company branding**
- **MUST use word "optional" and "separate"**
- **MUST include insurance partner disclaimers**
- API: `theme: "embedded_insurance"`

---

## 🎯 HOW TO MAKE A COMPLIANT VIDEO

### Step 1: Choose Theme
Pick one of the 6 approved themes above

### Step 2: Generate with Groq
```bash
POST /generate
{
    "topic": "Your topic here",
    "theme": "interview_prep",  # Use approved theme!
    "duration": 5,
    "quality": "720p",
    "auto_upload": true
}
```

### Step 3: Check Validation
Look at job status:
```json
"compliance_check": {
    "compliant": true,  // ✓ Good to publish!
    "violations": [],
    "warnings": []
}
```

### Step 4: Publish
If `compliant: true`, you're ready to go!

---

## 🚫 DON'T POSITION AS

- Insurance company
- Financial safety net
- Job loss prevention
- Income replacement
- Unemployment provider
- Employment agency
- Guaranteed protection

---

## ✅ DO POSITION AS

- AI career platform
- Career intelligence service
- Career development tools
- Interview preparation service
- Professional community
- Risk assessment service
- Career readiness provider

---

## 📝 KEY MESSAGING RULES

### When mentioning financial support:
- ✅ "Discretionary support"
- ✅ "At company discretion"
- ✅ "May provide"
- ❌ NOT "guaranteed"
- ❌ NOT "assured"
- ❌ NOT "will provide"

### Tone guidelines:
- ✅ Empowering, professional, modern, hopeful
- ❌ NOT fear-based, desperate, or overpromising

### Visual guidelines:
- ✅ Use navy (#0f172a) + green (#22c55e)
- ✅ Bright, professional environments
- ✅ Confident professionals using platform
- ✅ Modern dashboards and UIs
- ❌ NOT dark atmospheres
- ❌ NOT explicit layoff imagery
- ❌ NOT fear-based visuals

---

## 📋 PRE-PUBLISH CHECKLIST

- [ ] No forbidden terms used
- [ ] Using approved theme
- [ ] Discretionary support framed correctly (if mentioned)
- [ ] Tone is empowering, not fear-based
- [ ] Using brand colors (navy + green)
- [ ] Validation shows `compliant: true`
- [ ] YouTube description includes required disclaimer

---

## 🔗 VALIDATION ENDPOINTS

```bash
# Check if content is compliant
POST /compliance/validate-content
{
    "content": "your content here",
    "check_type": "strict"
}

# Get all approved themes
GET /compliance/themes

# Get full guidelines
GET /compliance/guidelines
```

---

## 💡 EXAMPLES

### ✅ CORRECT
"LayoffShield uses AI to assess your employment risk and provide personalized career guidance."

### ❌ WRONG
"LayoffShield provides job loss insurance to protect you from layoffs."

---

### ✅ CORRECT
"Discretionary financial support may be available to members at LayoffShield's discretion."

### ❌ WRONG
"We guarantee financial support if you get laid off."

---

### ✅ CORRECT
"Choose LayoffShield for career intelligence, interview prep, and community support."

### ❌ WRONG
"LayoffShield is your insurance against job loss."

---

## 📞 HELP

- **Full Guidelines**: See CONTENT_GUIDELINES.md
- **Implementation Details**: See COMPLIANCE_IMPLEMENTATION.md
- **API Response**: Check job status `compliance_check` field
- **Themes**: GET /compliance/themes

---

## ⚖️ LEGAL BASIS

**Tuli & Co Business Model Review** (April 2026):
- LayoffShield is NOT an insurance company IF operated as documented
- Discretionary support must remain voluntary and non-routine
- Marketing must NOT create expectation of guaranteed protection
- Insurance terminology is PROHIBITED in marketing

---

**Remember:** LayoffShield = Career Platform + Community  
**NOT:** Insurance Company + Financial Protection Service

---

*One-page quick reference | Last updated April 16, 2026*
