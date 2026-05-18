# LayoffShield Video Generation - Compliance Framework Implementation

**Implementation Date:** April 16, 2026  
**Framework Version:** 1.0  
**Compliance Reference:** Tuli & Co Business Model Review, April 18, 2026  

---

## Overview

I've successfully integrated LayoffShield's legal guidelines and company information into your video generation system. The framework ensures all generated videos strictly comply with regulatory requirements and brand positioning guidelines.

### ✅ What's Been Implemented

---

## 1. Comprehensive Compliance Framework

### File: `layoffshield_guidelines.py` (NEW - 380+ lines)

This is the backbone of the compliance system. It contains:

#### ✅ Forbidden Terminology List
Prevents use of words that could position LayoffShield as insurance:
- insurance, claim, premium, coverage, guaranteed payout, assured protection, etc.

#### ✅ Mandatory Alternative Terms
Approved replacements for each forbidden term:
```python
"insurance" → "membership" or "career support"
"claim" → "request"
"premium" → "subscription fee"
"coverage" → "protection package"
"guaranteed payout" → "discretionary support"
```

#### ✅ Six Approved Video Themes
Each with pre-validated messaging, visual guidelines, and do/don't rules:

1. **Risk Assessment** ("Know Your Risk")
   - Focus: Employment risk monitoring and AI analysis
   - Messaging: Data-driven, insightful, empowering

2. **AI Advisor** ("Personalized Career Guidance")
   - Focus: 24/7 AI career guidance
   - Messaging: Tailored, adaptive, supportive

3. **Interview Prep** ("Master Your Interview Skills")
   - Focus: AI-powered mock interviews
   - Messaging: Practice, feedback, confidence-building

4. **Career Readiness** ("Stay Career Ready")
   - Focus: Skill development and career resilience
   - Messaging: Proactive, empowering, forward-thinking

5. **Community** ("You're Not Alone")
   - Focus: Professional community and shared experience
   - Messaging: Supportive, inclusive, warm

6. **Embedded Insurance** (Premium tiers only)
   - Focus: Optional insurance from licensed partners
   - **CRITICAL**: Must show partner branding, use word "optional", clearly separate from LayoffShield

#### ✅ Brand Positioning
Clear definition of what LayoffShield IS and ISN'T:

| IS ✅ | IS NOT ❌ |
|------|----------|
| AI career platform | Insurance company |
| Risk assessment service | Financial safety net |
| Career development tools | Income replacement |
| Professional community | Unemployment provider |
| Interview coaching | Job guarantee service |

#### ✅ Compliance Validator Function
`validate_video_content()` function that checks any content for:
- Forbidden terminology
- Fear-based language
- Inappropriate framing
- Returns violations, warnings, and recommendations

#### ✅ Enhanced Groq System Prompt
Built-in compliance rules that instruct the AI to:
- Never position as insurance
- Use only approved terminology
- Follow approved messaging themes
- Maintain professional, empowering tone
- Show brand visuals and dashboards

---

## 2. Groq Service Enhancement

### File: `groq_service.py` (UPDATED)

**New Features:**

1. **Theme Parameter Support**
   ```python
   await generate_video_prompt(
       topic="AI mock interview feature",
       theme="interview_prep",  # NEW!
       validate=True            # NEW!
   )
   ```

2. **Returns Validation Results**
   ```json
   {
       "prompt": "generated video prompt...",
       "topic": "AI mock interview feature",
       "theme": "interview_prep",
       "compliant": true,
       "validation": {
           "violations": [],
           "warnings": [],
           "recommendations": [...],
           "flagged_terms": []
       }
   }
   ```

3. **Batch Generation**
   ```python
   await generate_video_prompt_batch([
       {"topic": "Risk assessment", "theme": "risk_assessment"},
       {"topic": "Interview prep", "theme": "interview_prep"},
   ])
   ```

4. **Better Logging**
   - Logs compliance warnings
   - Tracks validation results
   - Helps identify issues early

---

## 3. FastAPI Enhancements

### File: `main.py` (UPDATED)

**Three New Compliance Endpoints:**

#### 1. Get Compliance Guidelines
```bash
GET /compliance/guidelines
```
Returns:
- All approved themes
- Mandatory disclaimers
- Company legal status
- Core services list

#### 2. Validate Content
```bash
POST /compliance/validate-content
{
    "content": "Your video prompt here",
    "check_type": "strict"  # or "warning"
}
```
Returns violations and recommendations

#### 3. List Approved Themes
```bash
GET /compliance/themes
```
Returns all 6 approved themes with full messaging framework

**Updated Endpoints:**

#### Video Generation
```bash
POST /generate
{
    "topic": "string - marketing topic",
    "theme": "string - approved theme (NEW!)",
    "duration": 5,
    "quality": "720p",
    "auto_upload": true,
    "youtube_title": "string",
    "youtube_description": "string",
    "youtube_tags": ["array"]
}
```

#### Job Status Response
Now includes compliance check results:
```json
{
    "job_id": "...",
    "status": "done",
    "prompt_used": "...",
    "compliance_check": {
        "compliant": true,
        "violations": [],
        "warnings": [],
        "recommendations": []
    },
    "video_url": "...",
    "youtube_url": "..."
}
```

**Updated Pipeline:**
- Generates prompt with Groq
- Validates compliance
- Logs warnings if issues found
- Stores validation results in job
- Allows human review of compliance issues

**Updated YouTube Description:**
- Uses compliant terminology
- Includes required disclaimer
- Removes forbidden terms
- Uses approved hashtags

---

## 4. Content Guidelines Reference

### File: `CONTENT_GUIDELINES.md` (NEW - Comprehensive Reference)

A complete reference guide (6,000+ words) covering:

1. **Critical Compliance Rules**
   - Why LayoffShield is NOT insurance
   - Forbidden terms and alternatives
   - How to frame financial support

2. **Brand Positioning Framework**
   - What LayoffShield IS
   - What LayoffShield IS NOT
   - Core value proposition

3. **Approved Messaging Themes**
   - 6 complete theme frameworks
   - Approved messaging for each
   - Visual guidelines
   - Do/Don't rules

4. **Visual Identity**
   - Brand colors (navy #0f172a + green #22c55e)
   - Professional mood guidelines
   - Environment examples
   - What to avoid visually

5. **Platform-Specific Guidelines**
   - YouTube description format
   - Approved hashtags
   - Social media guidelines
   - Email campaign rules

6. **Validation Checklist**
   - Terminology check
   - Positioning check
   - Tone check
   - Visual check
   - Disclaimer check

---

## 🎯 How to Use the System

### 1. Generate a Compliant Video

**Option A: Using Approved Theme**
```bash
POST /generate
{
    "topic": "Master your interviews with AI practice",
    "theme": "interview_prep",
    "duration": 5,
    "quality": "720p",
    "auto_upload": true,
    "youtube_title": "Interview Mastery with LayoffShield",
    "youtube_tags": ["LayoffShield", "InterviewPrep"]
}
```

**Option B: Without Theme**
```bash
POST /generate
{
    "topic": "AI-powered career readiness tools",
    "duration": 5,
    "quality": "720p"
}
```

### 2. Check Compliance

```bash
POST /compliance/validate-content
{
    "content": "Your video prompt or script here",
    "check_type": "strict"
}
```

Response:
```json
{
    "compliant": true,
    "violations": [],
    "warnings": [],
    "recommendations": ["✓ Content appears compliant"],
    "flagged_terms": []
}
```

### 3. View Available Themes

```bash
GET /compliance/themes
```

Returns:
```json
{
    "risk_assessment": {
        "title": "Know Your Risk",
        "messaging": [...],
        "visual_focus": "...",
        "do": [...],
        "dont": [...]
    },
    "ai_advisor": {...},
    "interview_prep": {...},
    ...
}
```

### 4. Get Compliance Guidelines

```bash
GET /compliance/guidelines
```

Returns company info, approved themes, mandatory disclaimers, etc.

---

## ✅ Compliance Checklist

Before publishing any video, verify:

- [ ] **Terminology**: No forbidden words (insurance, claim, premium, etc.)
- [ ] **Positioning**: Platform positioned as career tool, NOT insurance
- [ ] **Support Framing**: Financial support (if mentioned) is "discretionary, not guaranteed"
- [ ] **Theme**: Uses one of 6 approved themes
- [ ] **Tone**: Empowering and professional, not fear-based
- [ ] **Visuals**: Uses brand colors (navy + green), bright environments
- [ ] **Disclaimers**: Includes required disclaimers where relevant
- [ ] **Validation Passed**: Validation results show compliant: true

---

## 🚫 Key Constraints from Legal Review

### 1. NOT Insurance
- Cannot be positioned or marketed as insurance
- Cannot use insurance terminology
- Cannot make guaranteed financial promises
- Cannot imply insurance protection

### 2. Discretionary Support
- Financial support is at company discretion
- NOT automatically provided
- NOT guaranteed to members
- Subject to case-by-case evaluation

### 3. Brand Tone
- Empowering, not fear-based
- Trustworthy and professional
- Forward-thinking and modern
- Human-centric (not desperate)

### 4. Messaging Focus
- Career intelligence and risk assessment
- Skill development and interview prep
- Professional community and support
- Career readiness tools

### 5. Embedded Insurance
- Optional, separate offering (premium tiers)
- Must show licensed partner's branding
- Must use word "optional"
- Must include partner's disclaimers

---

## 📊 Example Workflow

### Scenario: Create Video About Interview Prep

```bash
# Step 1: Get theme details
GET /compliance/themes

# Step 2: Create video with approved theme
POST /generate
{
    "topic": "Practice interviews with AI feedback",
    "theme": "interview_prep",
    "duration": 5,
    "auto_upload": true,
    "youtube_title": "Master Your Interviews with AI-Powered Practice"
}

# Step 3: Monitor job status
GET /jobs/{job_id}

# Response includes:
{
    "status": "done",
    "compliance_check": {
        "compliant": true,
        "violations": [],
        "warnings": [],
        "recommendations": ["✓ Content appears compliant"]
    },
    "prompt_used": "vivid cinematic video prompt...",
    "video_url": "/downloads/video123.mp4",
    "youtube_url": "https://youtube.com/watch?v=..."
}
```

---

## 🔍 Understanding Validation Results

### Compliance: true
✅ Content is fully compliant with guidelines  
✅ Safe to publish  
✅ All terminology approved  
✅ Messaging framework correct  

### Compliance: false
❌ Content has violations  
❌ Review violations before publishing  
❌ Update content to use approved terminology  
❌ Re-validate before publishing  

### Violations
Serious issues that must be fixed:
- Forbidden terminology used
- Positioning violates guidelines
- False guarantees made
- Insurance language used

### Warnings
Potential issues that should be reviewed:
- Fear-based language detected
- Potentially problematic framing
- May need clarification

### Recommendations
Suggestions for improvement:
- Replace term X with Y
- Clarify this statement
- Ensure tone is empowering, not fear-based
- Add required disclaimer

---

## 📝 Key Points to Remember

1. **LayoffShield is NOT insurance** - This is the #1 rule
2. **Use approved themes** - 6 pre-validated messaging frameworks available
3. **Use alternative terminology** - Don't say "insurance", say "membership"
4. **Frame support as discretionary** - Never guarantee financial support
5. **Maintain empowering tone** - Professional, trustworthy, forward-thinking
6. **Validate before publishing** - Use API endpoint or review checklist
7. **Include required disclaimers** - Especially for YouTube descriptions
8. **Show partner branding** - If featuring embedded insurance
9. **Track compliance status** - Check compliance_check in job response
10. **Refer to CONTENT_GUIDELINES.md** - When in doubt, consult the reference

---

## 🎨 Brand Identity Quick Reference

### Colors
- **Navy**: #0f172a (professional, trustworthy)
- **Green**: #22c55e (energetic, positive)
- **Blue**: #0ea5e9 (tech, innovation)

### Tone
- Empowering (not rescue-based)
- Trustworthy (not salesy)
- Modern (not outdated)
- Hopeful (not fear-based)
- Professional (not casual)

### Environments
- Modern offices and workspaces
- Home office setups (professional)
- Bright, well-lit spaces
- Collaborative environments
- Technology company aesthetics

### What To Avoid
- Dark, depressing settings
- Explicit layoff/firing visuals
- Desperate or stressed people
- Fear-based imagery
- Generic stock footage

---

## 📚 Reference Files

1. **layoffshield_guidelines.py** - Complete compliance framework (380+ lines)
2. **groq_service.py** - Enhanced prompt generation with validation
3. **main.py** - Updated FastAPI with compliance endpoints
4. **CONTENT_GUIDELINES.md** - Comprehensive reference guide (this file)

---

## 🚀 Getting Started

1. **Read CONTENT_GUIDELINES.md** - Familiarize yourself with themes and rules
2. **Test `/compliance/themes`** - See all available themes
3. **Try generating a video** - Use an approved theme
4. **Check compliance results** - Review validation in job status
5. **Validate your own content** - Use `/compliance/validate-content` endpoint

---

## ❓ Questions?

Refer to:
- **CONTENT_GUIDELINES.md** - For messaging and visual rules
- **API endpoints** - For theme details and validation
- **Validation results** - For specific compliance issues
- **Code comments** - For implementation details

---

**Framework Status:** ✅ ACTIVE  
**All Video Content Must Comply:** YES  
**Legal Reference:** Tuli & Co Business Model Review, April 2026  

---

*Last Updated: April 16, 2026*  
*Version: 1.0 - Initial Implementation*
