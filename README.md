# 🛡️ LayoffShield Marketing Automation

Auto-generates cinematic marketing videos for LayoffShield and posts them to YouTube.

## Pipeline

```
Topic input
    → Groq LLaMA 3.3 70B  → cinematic video prompt
    → PixVerse web UI     → 720p MP4 video (browser session)
    → YouTube Data API v3 → auto-posted to your channel
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Get your API keys

**Groq API Key**
- https://console.groq.com → API Keys

**PixVerse Web Login**
- https://app.pixverse.ai/login → sign in once in the browser window
- The app stores the PixVerse browser session in `.pixverse-playwright/`
- No PixVerse API key is required for this flow

**Google / YouTube OAuth**
1. https://console.cloud.google.com → New Project
2. APIs & Services → Enable → "YouTube Data API v3"
3. OAuth consent screen → External → add your Gmail as test user
4. Credentials → Create OAuth 2.0 Client ID → Web Application
5. Authorized redirect URI: `http://localhost:8000/auth/youtube/callback`
6. Copy Client ID + Client Secret into `.env`

### 4. Run
```bash
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000 in your browser.

### 5. Authenticate YouTube (one-time)
- Click **Connect YouTube** in the dashboard header
- Sign in with Google → Allow permissions
- Done! Token is saved to `youtube_token.json` and auto-refreshed forever.

## Usage

### Via Dashboard (http://localhost:8000)
1. Enter a topic: e.g. "AI mock interview feature demo"
2. Pick duration (5s recommended on free tier for credits)
3. Toggle auto-upload to YouTube
4. Click **Generate & Post Video**
5. Watch the pipeline status update live

### Via API directly
```bash
# Generate video + auto-post to YouTube
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "layoff risk analysis for tech employees",
    "duration": 5,
    "quality": "720p",
    "auto_upload": true
  }'

# Check job status
curl http://localhost:8000/jobs/{job_id}
```

## PixVerse Free Tier Notes

- ✅ Text-to-video generation: SUPPORTED
- ✅ Max resolution: 720p
- ✅ Max concurrency: 3 simultaneous jobs
- ✅ Models: v3.5, v4, v4.5, v5
- ⚠️  motion_mode "fast" = 2× credits consumed
- ⚠️  5-second 720p video costs 60 credits
- 💡  Recommended: 5s duration at 720p for best credit efficiency

## File Structure

```
layoffshield_marketing/
├── main.py              # FastAPI app + pipeline orchestration
├── config.py            # Settings (reads from .env)
├── groq_service.py      # Groq LLM → video prompts
├── pixverse_browser_service.py  # PixVerse browser automation via Playwright
├── youtube_service.py   # YouTube OAuth + upload
├── dashboard.html       # Web UI
├── requirements.txt
└── .env.example
```
