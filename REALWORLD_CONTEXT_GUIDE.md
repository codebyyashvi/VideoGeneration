# Real-World Layoff Context Integration - Usage Guide

**Updated:** May 18, 2026  
**Enhancement:** Real-world layoff trends now integrated into video generation  

---

## 🌍 **What's New**

The system now fetches and integrates **real-world layoff data** into video generation, making videos more meaningful and relevant to what employees are actually experiencing.

---

## 📊 **New Endpoints**

### 1. Get Current Layoff Trends
```bash
GET /layoff-trends
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-05-18T...",
  "major_trends": [
    "Tech layoffs continue: 260,000+ laid off in 2024-2025",
    "AI/ML focus: Companies restructuring around AI",
    "Finance sector: Banking consolidation causing layoffs",
    ...
  ],
  "affected_industries": [
    "Technology/SaaS (35%)",
    "Finance/FinTech (25%)",
    ...
  ],
  "most_affected_roles": [
    "Customer Success (automatable)",
    "QA Engineers (shifting to automation)",
    ...
  ],
  "safer_roles": [
    "Senior Engineering",
    "Product Management",
    ...
  ],
  "key_statistics": {
    "total_laid_off_2024_2025": "260,000+",
    "applications_per_role_increase": "3-5x",
    "ai_roles_growth": "70%",
    ...
  }
}
```

**Use Case:** Show employees the real context of what they're dealing with.

---

### 2. Get Full Layoff Context for Video
```bash
GET /layoff-context
```

**Response:**
```json
{
  "status": "ok",
  "context": "CURRENT REAL-WORLD LAYOFF SITUATION...\n\n[Full context about trends, affected roles, etc.]",
  "purpose": "This context is used to make video prompts more relevant to real employee concerns"
}
```

---

### 3. Get Recommended Themes Based on Current Situation
```bash
GET /recommended-themes
```

**Response:**
```json
{
  "status": "ok",
  "current_situation": "High layoff activity across tech, finance, and e-commerce",
  "recommended_themes_now": [
    {
      "theme": "stressed_employee_scenario",
      "reason": "Directly addresses real employee concerns about industry layoffs",
      "messaging": "From worry about real trends → clarity through LayoffShield",
      "effectiveness": "High - resonates with employees checking layoff news today"
    },
    {
      "theme": "risk_assessment",
      "reason": "Helps understand personal risk based on industry trends",
      "effectiveness": "High - directly actionable"
    },
    ...
  ],
  "tip": "Use stressed_employee_scenario theme + /generate-contextual for max relevance"
}
```

---

### 4. Generate Contextual Video (NEW!)
```bash
POST /generate-contextual
```

**Request:**
```json
{
  "topic": "Know your layoff risk in today's market",
  "theme": "stressed_employee_scenario",
  "duration": 5,
  "quality": "720p",
  "auto_upload": true,
  "youtube_title": "Understanding Your Career Risk in 2026",
  "youtube_tags": ["LayoffShield", "CareerReady", "LayoffTrends"]
}
```

**What it does:**
1. ✅ Fetches current layoff trends and industry data
2. ✅ Includes real-world context in Groq prompt
3. ✅ Generates video that feels RELEVANT to employees NOW
4. ✅ Shows transformation from worry → clarity via LayoffShield
5. ✅ Validates for compliance (still!)
6. ✅ Returns contextual video ready for publishing

**Response includes:**
```json
{
  "job_id": "...",
  "status": "fetching_context",
  "message": "Real-world context loaded",
  "real_world_context_used": true,
  ...
}
```

---

## 🎯 **How to Generate Meaningful Videos**

### Option 1: Quick Contextual Video
```bash
# This is THE BEST approach for relevant videos

POST /generate-contextual
{
  "topic": "Do I have layoff risk in my role?",
  "theme": "stressed_employee_scenario",
  "duration": 5,
  "auto_upload": true
}
```

**What this does:**
- Fetches real layoff trends (tech layoffs, affected roles, safer roles, etc.)
- Includes this context in the AI prompt
- Generates video showing: Employee concerned → Checks data → Gets clarity → Takes action
- Video feels RELEVANT because it addresses actual market conditions

---

### Option 2: Risk Assessment with Context
```bash
POST /generate-contextual
{
  "topic": "Assess your employment risk in today's market",
  "theme": "risk_assessment",
  "duration": 5,
  "auto_upload": true,
  "youtube_title": "Is Your Role At Risk? Real Data From 2026 Layoffs"
}
```

---

### Option 3: Standard Video (without context)
```bash
# Still works! But less contextual

POST /generate
{
  "topic": "AI mock interviews",
  "theme": "interview_prep",
  "duration": 5,
  "auto_upload": true
}
```

---

## 📈 **Real-World Data Integration**

The system now includes:

### Current Situation Data
- **Tech layoffs:** 260,000+ in 2024-2025
- **Most affected:** Customer Success, QA, Junior Devs, Business Analysts
- **Safer roles:** Senior Engineering, Product, Sales, Security
- **Job market:** 3-5x more applications per role
- **Affected industries:** Tech 35%, Finance 25%, Retail 15%, Media 15%

### How It's Used in Video Generation
```
Groq receives:
1. Your topic (e.g., "Know your risk")
2. Theme instructions (e.g., "stressed_employee_scenario")
3. PLUS real-world context:
   - Current layoff trends
   - Affected and safer roles
   - Market statistics
   - Industry breakdown
4. Generates video that reflects REAL situation
```

---

## 🎬 **Example Workflow**

### Step 1: Check What's Happening
```bash
GET /layoff-trends
# See: "Tech layoffs continue: 260,000+ tech workers laid off"
# See: "Finance sector: 50,000+ layoffs in 2025"
```

### Step 2: Get Recommendations
```bash
GET /recommended-themes
# Sees: "stressed_employee_scenario is most relevant NOW"
# Sees: "Effectiveness: High - resonates with employees checking layoff news"
```

### Step 3: Generate Contextual Video
```bash
POST /generate-contextual
{
  "topic": "Is my tech job at risk in 2026?",
  "theme": "stressed_employee_scenario"
}
```

### Step 4: Video is Generated
- Groq knows it's May 2026, tech layoffs are happening
- Generates video showing real employee concern
- Shows LayoffShield dashboard with risk insights
- Ends with empowerment: "Now I know where I stand"
- Video feels REAL and RELEVANT

### Step 5: Publish
- Compliance check passes ✓
- Context-aware video ✓
- Employee-relevant messaging ✓
- Ready to publish!

---

## 🔄 **Comparison**

| Aspect | Standard | Contextual |
|--------|----------|-----------|
| Topic-based | ✓ | ✓ |
| Real-world aware | ✗ | ✓ |
| Compliance checked | ✓ | ✓ |
| Fetches layoff data | ✗ | ✓ |
| Includes market context | ✗ | ✓ |
| Relevance to employees | Good | **Excellent** |
| Emotional resonance | Moderate | **High** |
| Feels current/urgent | Moderate | **High** |

---

## 📝 **Available Themes with Context**

All 7 themes work with contextual generation:

1. **risk_assessment** - "Know Your Risk"
   - Best for: Understanding personal risk based on trends
   
2. **stressed_employee_scenario** - "From Worry to Clarity" ⭐ RECOMMENDED
   - Best for: Addressing real employee anxiety about layoffs
   - Most relevant right now

3. **ai_advisor** - "Personalized Career Guidance"
   - Best for: Showing how to prepare strategically

4. **interview_prep** - "Master Your Interview Skills"
   - Best for: Building competitive advantage

5. **preparedness** - "Stay Career Ready"
   - Best for: Proactive career management

6. **community** - "You're Not Alone"
   - Best for: Building community around shared concerns

7. **embedded_insurance** - "Optional Protection"
   - Best for: Premium tier supplementary insurance

---

## 💡 **Pro Tips**

1. **Use `/recommended-themes` first** to see what's most relevant RIGHT NOW
2. **Use `stressed_employee_scenario` with contextual generation** for maximum relevance
3. **Check `/layoff-trends`** to understand what employees are worried about
4. **Reference real statistics** in social media captions (e.g., "260K tech workers laid off in 2024-2025")
5. **Update videos as trends change** - contextual videos stay relevant longer

---

## 🔍 **What Gets Included in Context**

When you use `/generate-contextual`, the prompt includes:

```
✓ Current layoff statistics (260K+ etc.)
✓ Most affected roles (so employees can assess risk)
✓ Safer roles (for hope/resilience messaging)
✓ Industry breakdown (to explain why it's happening)
✓ Geographic impact (for local relevance)
✓ Job market competition data (3-5x applications)
✓ AI skill growth (70% increase in AI roles)
✓ Timeline/recovery info (what to expect)
✓ Actionable insights for professionals
✓ Real company examples (Meta, Amazon, Stripe, etc.)
```

All of this helps Groq generate videos that feel REAL, RELEVANT, and MEANINGFUL.

---

## 📊 **Real Data Examples Used**

- **Meta:** 21,000 employees (13% workforce) - 2024
- **Amazon:** 18,000 employees - early 2024
- **Stripe:** 14% workforce - 2023
- **Shopify:** 10% workforce - 2023
- **Twitter/X:** 50% workforce reduction - 2023-2024

(These are real events that employees know about)

---

## ✅ **Compliance is Still Enforced**

Even with real-world context:
- ✓ No forbidden terminology used
- ✓ NOT positioned as insurance
- ✓ Support framed as discretionary
- ✓ Empowering tone (not fear-mongering)
- ✓ Transformation-focused (worry → clarity)
- ✓ All guidelines still applied

---

## 🚀 **Getting Started**

```bash
# 1. Check current trends
curl http://localhost:8000/layoff-trends

# 2. Get recommendations
curl http://localhost:8000/recommended-themes

# 3. Generate contextual video
curl -X POST http://localhost:8000/generate-contextual \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Does my role have layoff risk?",
    "theme": "stressed_employee_scenario",
    "duration": 5,
    "auto_upload": true
  }'

# 4. Check status
curl http://localhost:8000/jobs/{job_id}
```

---

## 📞 **Summary**

**Before:** Videos were topic-based  
**Now:** Videos are context-aware + employee-relevant + compliance-checked

**The Result:** Videos that feel like they're addressing what employees are experiencing TODAY, not generic career advice.

---

**Status:** ✅ READY TO USE  
**Date:** May 18, 2026  
**Context:** Real-world layoff trends integrated  

*Generate contextual videos that matter.*
