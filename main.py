"""
LayoffShield Marketing Automation - FastAPI Backend
Generates AI marketing videos and auto-posts to YouTube
"""

import os
import sys
import uuid
import asyncio
import httpx
import json
import time
from pathlib import Path
from typing import Optional

# Windows event loop fix for Playwright subprocess support
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq_service import generate_video_prompt
from pixverse_browser_service import generate_video, poll_video_status, download_video
from youtube_service import upload_to_youtube, get_oauth_url, handle_oauth_callback, is_authenticated
from config import settings
from layoffshield_guidelines import (
    validate_video_content,
    APPROVED_VIDEO_THEMES,
    MANDATORY_DISCLAIMERS,
)
from layoff_news_fetcher import (
    fetch_layoff_trends,
    get_layoff_statistics,
    get_layoff_context_for_video,
)

app = FastAPI(title="LayoffShield Marketing Automation", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (use Redis/DB in production)
jobs: dict = {}

# ─────────────────────────────────────────────
# Request / Response models
# ─────────────────────────────────────────────

class VideoRequest(BaseModel):
    topic: str  # e.g. "AI mock interview feature", "layoff risk analysis"
    theme: Optional[str] = None  # Optional approved theme (risk_assessment, ai_advisor, interview_prep, etc)
    duration: int = 5  # seconds, 5-10 on free tier 720p
    quality: str = "720p"  # 360p | 540p | 720p (free tier max)
    aspect_ratio: str = "16:9"
    style: Optional[str] = None  # realistic | anime | 3d_animation
    auto_upload: bool = True
    youtube_title: Optional[str] = None
    youtube_description: Optional[str] = None
    youtube_tags: Optional[list[str]] = None

class JobStatus(BaseModel):
    job_id: str
    status: str
    message: str
    video_url: Optional[str] = None
    youtube_url: Optional[str] = None
    prompt_used: Optional[str] = None
    error: Optional[str] = None
    compliance_check: Optional[dict] = None  # Validation results


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(Path(__file__).parent / "dashboard.html", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "LayoffShield Marketing Bot"}


# ── YouTube OAuth ──────────────────────────────

@app.get("/auth/youtube")
async def youtube_auth():
    """Start YouTube OAuth flow"""
    url = get_oauth_url()
    return RedirectResponse(url=url)


@app.get("/auth/youtube/callback")
async def youtube_callback(code: str, state: Optional[str] = None):
    """Handle OAuth callback from Google"""
    success = handle_oauth_callback(code)
    if success:
        return HTMLResponse("""
        <html><body style='font-family:sans-serif;text-align:center;padding:60px;background:#0f172a;color:#22c55e'>
        <h1>✅ YouTube Connected!</h1>
        <p style='color:#94a3b8'>You can now close this tab and start generating videos.</p>
        <script>setTimeout(()=>window.close(),3000)</script>
        </body></html>
        """)
    raise HTTPException(status_code=400, detail="OAuth failed")


@app.get("/auth/status")
async def auth_status():
    return {"youtube_connected": is_authenticated()}


# ── Compliance & Guidelines ────────────────────

@app.get("/compliance/guidelines")
async def get_guidelines():
    """Get LayoffShield compliance guidelines for video content"""
    return {
        "approved_themes": list(APPROVED_VIDEO_THEMES.keys()),
        "themes_detail": {k: {"theme": v["theme"], "messaging": v["messaging"]} 
                         for k, v in APPROVED_VIDEO_THEMES.items()},
        "mandatory_disclaimers": MANDATORY_DISCLAIMERS,
        "company_info": {
            "legal_status": "NOT an insurance company",
            "core_services": [
                "Employment risk monitoring & AI-driven risk scoring",
                "Personalized AI career advisor",
                "AI-powered mock interview practice",
                "Skill gap analysis & career development",
                "Community and support resources",
            ],
        }
    }


@app.post("/compliance/validate-content")
async def validate_content(request: dict):
    """Validate video prompt or description for compliance"""
    content = request.get("content", "")
    check_type = request.get("check_type", "strict")  # strict | warning
    
    if not content:
        raise HTTPException(status_code=400, detail="content field required")
    
    result = validate_video_content(content, check_type)
    return result


@app.get("/compliance/themes")
async def list_themes():
    """List approved video themes and messaging"""
    return {
        theme_name: {
            "title": theme_data["theme"],
            "messaging": theme_data["messaging"],
            "visual_focus": theme_data["visual_focus"],
            "do": theme_data.get("do", []),
            "dont": theme_data.get("dont", []),
        }
        for theme_name, theme_data in APPROVED_VIDEO_THEMES.items()
    }


# ── Real-World Layoff Context ──────────────────

@app.get("/layoff-trends")
async def get_layoff_trends():
    """
    Get current real-world layoff trends and statistics.
    Used to make videos more contextual and meaningful to employee concerns.
    """
    try:
        trends = await fetch_layoff_trends()
        stats = get_layoff_statistics()
        return {
            "status": "ok",
            "timestamp": trends.get("as_of"),
            "major_trends": trends.get("major_trends", []),
            "affected_industries": trends.get("affected_industries", []),
            "most_affected_roles": trends.get("most_affected_roles", []),
            "safer_roles": trends.get("least_affected_roles", []),
            "key_statistics": stats,
            "actionable_insights": trends.get("actionable_insights_for_professionals", []),
            "geographic_impact": trends.get("geographic_impact", {}),
            "message": "These are real trends employees are facing. LayoffShield helps them prepare.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not fetch layoff trends: {e}",
            "fallback": "Using curated data based on 2024-2025 trends",
        }


@app.get("/layoff-context")
async def get_context_for_video_generation():
    """
    Get the full context about current layoff situation.
    This is injected into Groq prompts to make videos more meaningful.
    """
    try:
        context = await get_layoff_context_for_video()
        return {
            "status": "ok",
            "context": context,
            "purpose": "This context is used to make video prompts more relevant to real employee concerns",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not generate context: {e}",
        }


@app.post("/generate-contextual", response_model=JobStatus)
async def generate_contextual_marketing_video(req: VideoRequest, background_tasks: BackgroundTasks):
    """
    Generate video with REAL-WORLD CONTEXT about current layoffs.
    This creates more meaningful, relevant videos that address actual employee concerns.
    
    The system will:
    1. Fetch current layoff trends and industry data
    2. Include this context in the Groq prompt
    3. Generate a video that feels relevant to what employees are experiencing NOW
    4. Show transformation from concern about real trends → clarity from LayoffShield
    """
    if req.auto_upload and not is_authenticated():
        raise HTTPException(
            status_code=401,
            detail="YouTube not authenticated. Visit /auth/youtube first."
        )

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "queued",
        "message": "Job queued for contextual video generation",
        "video_url": None,
        "youtube_url": None,
        "prompt_used": None,
        "error": None,
        "youtube_title": req.youtube_title,
        "youtube_description": req.youtube_description,
        "youtube_tags": req.youtube_tags,
        "auto_upload": req.auto_upload,
        "is_contextual": True,
    }

    background_tasks.add_task(run_contextual_pipeline, job_id, req)

    return JobStatus(
        job_id=job_id,
        status="queued",
        message="Pipeline started with real-world context. Poll /jobs/{job_id} for status.",
    )


# ── Suggested Themes Endpoint ──────────────────

@app.get("/recommended-themes")
async def get_recommended_themes():
    """
    Get RECOMMENDED themes based on current layoff situation.
    Shows which themes are most relevant RIGHT NOW.
    """
    return {
        "status": "ok",
        "current_situation": "High layoff activity across tech, finance, and e-commerce sectors",
        "recommended_themes_now": [
            {
                "theme": "stressed_employee_scenario",
                "reason": "Directly addresses real employee concerns about industry layoffs",
                "messaging": "From worry about real trends → clarity through LayoffShield data",
                "effectiveness": "High - resonates with employees checking layoff news today",
            },
            {
                "theme": "risk_assessment",
                "reason": "Helps employees understand their personal risk based on industry trends",
                "messaging": "Know where you stand in the current market",
                "effectiveness": "High - directly actionable",
            },
            {
                "theme": "interview_prep",
                "reason": "Employees are updating skills due to competitive job market",
                "messaging": "Be interview-ready if you need to move",
                "effectiveness": "Medium-High - secondary concern after risk",
            },
            {
                "theme": "community",
                "reason": "Employees want to connect with others in similar situations",
                "messaging": "You're not alone - support from people experiencing the same",
                "effectiveness": "Medium - emotional support angle",
            },
        ],
        "less_relevant_now": [
            {
                "theme": "preparedness",
                "reason": "Valid but less urgent than assessing current personal risk",
            },
        ],
        "tip": "Use stressed_employee_scenario theme + /generate-contextual endpoint for maximum relevance",
    }


# ── Pipeline ───────────────────────────────────

@app.post("/generate", response_model=JobStatus)
async def generate_marketing_video(req: VideoRequest, background_tasks: BackgroundTasks):
    """
    Full pipeline: Groq → prompt → PixVerse → video → YouTube
    """
    if req.auto_upload and not is_authenticated():
        raise HTTPException(
            status_code=401,
            detail="YouTube not authenticated. Visit /auth/youtube first."
        )

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "queued",
        "message": "Job queued",
        "video_url": None,
        "youtube_url": None,
        "prompt_used": None,
        "error": None,
        "youtube_title": req.youtube_title,
        "youtube_description": req.youtube_description,
        "youtube_tags": req.youtube_tags,
        "auto_upload": req.auto_upload,
    }

    background_tasks.add_task(run_pipeline, job_id, req)

    return JobStatus(
        job_id=job_id,
        status="queued",
        message="Pipeline started. Poll /jobs/{job_id} for status.",
    )


@app.post('/jobs/{job_id}/fetch')
async def fetch_job(job_id: str, background_tasks: BackgroundTasks):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail='Job not found')
    background_tasks.add_task(fetch_and_open_job, job_id)
    return JSONResponse({'status':'started', 'message':'Fetching video in background'})


@app.post('/jobs/{job_id}/upload')
async def upload_job(job_id: str, background_tasks: BackgroundTasks):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail='Job not found')
    background_tasks.add_task(upload_job_video, job_id)
    return JSONResponse({'status':'started', 'message':'Upload started in background'})


@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    j = jobs[job_id]
    return JobStatus(job_id=job_id, **j)


@app.get("/jobs")
async def list_jobs():
    return [{"job_id": k, **v} for k, v in jobs.items()]


@app.get("/downloads/{filename}")
async def serve_download(filename: str):
    """Serve files from the configured download directory."""
    path = Path(settings.download_dir) / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


# Legacy path support: some clients request the raw /tmp/layoffshield_videos/... URL
@app.get("/tmp/layoffshield_videos/{filename}")
async def serve_legacy_tmp(filename: str):
    path = Path(settings.download_dir) / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


# ── Pipeline ───────────────────────────────────

async def run_pipeline(job_id: str, req: VideoRequest):
    def update(status, message, **kwargs):
        jobs[job_id].update({"status": status, "message": message, **kwargs})

    try:
        # Step 1: Generate prompt with Groq (includes compliance validation)
        update("generating_prompt", "🤖 Generating marketing prompt with Groq...")
        prompt_result = await generate_video_prompt(
            req.topic, 
            theme=req.theme, 
            validate=True,
            include_realworld_context=False  # Standard pipeline without context
        )
        
        prompt_text = prompt_result["prompt"]
        is_compliant = prompt_result["compliant"]
        validation_info = prompt_result["validation"]
        
        # Store prompt and validation results
        jobs[job_id]["prompt_used"] = prompt_text
        jobs[job_id]["compliance_check"] = validation_info
        
        # Log compliance status
        if not is_compliant:
            update(
                "generating_prompt", 
                "⚠️ Prompt has compliance issues - review before publishing",
                prompt_used=prompt_text,
                compliance_check=validation_info
            )
            print(f"[COMPLIANCE WARNING] Job {job_id}: {validation_info['violations']}")
        else:
            update("generating_prompt", "✅ Prompt ready and compliance-checked", prompt_used=prompt_text)

        # Step 2: Submit to PixVerse
        update("generating_video", "🎬 Submitting to PixVerse for video generation...")
        video_id = await generate_video(
            prompt=prompt_text,
            duration=req.duration,
            quality=req.quality,
            aspect_ratio=req.aspect_ratio,
            style=req.style,
        )

        # Job now waits for user to 'See Video' to fetch it
        update("waiting_for_user", "🟡 Video submitted — click 'See Video' to open and fetch generated video", prompt_used=prompt_text)
        # store video generation token so fetch endpoint can use it
        jobs[job_id]["generation_token"] = video_id
    except Exception as e:
        jobs[job_id].update({"status": "error", "message": "Pipeline failed", "error": str(e)})
        raise


async def run_contextual_pipeline(job_id: str, req: VideoRequest):
    """
    Generate video WITH real-world layoff context integrated.
    This creates more meaningful, relevant videos.
    """
    def update(status, message, **kwargs):
        jobs[job_id].update({"status": status, "message": message, **kwargs})

    try:
        # Step 1: Fetch and prepare real-world context
        update("fetching_context", "📊 Fetching current layoff trends and market data...")
        try:
            context = await get_layoff_context_for_video()
            update("fetching_context", "✅ Real-world context loaded", context_loaded=True)
        except Exception as e:
            logger.warning(f"Could not fetch context: {e}")
            update("fetching_context", "⚠️ Using fallback context data", context_loaded=False)
        
        # Step 2: Generate prompt WITH context
        update("generating_prompt", "🤖 Generating contextual prompt with Groq + real-world data...")
        
        # If theme not specified, recommend stressed_employee_scenario for context
        theme = req.theme if req.theme else "stressed_employee_scenario"
        
        prompt_result = await generate_video_prompt(
            req.topic, 
            theme=theme, 
            validate=True,
            include_realworld_context=True  # INCLUDE real-world context
        )
        
        prompt_text = prompt_result["prompt"]
        is_compliant = prompt_result["compliant"]
        validation_info = prompt_result["validation"]
        context_included = prompt_result.get("real_world_context_included", False)
        
        # Store prompt and validation results
        jobs[job_id]["prompt_used"] = prompt_text
        jobs[job_id]["compliance_check"] = validation_info
        jobs[job_id]["real_world_context_used"] = context_included
        
        # Log status
        if not is_compliant:
            update(
                "generating_prompt", 
                "⚠️ Prompt has compliance issues - review before publishing",
                prompt_used=prompt_text,
                compliance_check=validation_info,
                real_world_context=context_included
            )
        else:
            context_msg = " + real-world context" if context_included else ""
            update(
                "generating_prompt", 
                f"✅ Contextual prompt ready{context_msg}", 
                prompt_used=prompt_text,
                real_world_context=context_included
            )

        # Step 3: Submit to PixVerse
        update("generating_video", "🎬 Submitting contextual video to PixVerse...")
        video_id = await generate_video(
            prompt=prompt_text,
            duration=req.duration,
            quality=req.quality,
            aspect_ratio=req.aspect_ratio,
            style=req.style,
        )

        update("waiting_for_user", "🟡 Contextual video submitted — click 'See Video' to fetch", prompt_used=prompt_text)
        jobs[job_id]["generation_token"] = video_id
        
    except Exception as e:
        jobs[job_id].update({"status": "error", "message": "Contextual pipeline failed", "error": str(e)})
        raise


async def fetch_and_open_job(job_id: str):
    """Background task: poll PixVerse for the given job's generation token and update job with video_url."""
    if job_id not in jobs:
        return
    j = jobs[job_id]
    token = j.get("generation_token")
    if not token:
        j.update({"status": "error", "message": "No generation token for job"})
        return
    j.update({"status": "fetching", "message": "🔎 Opening PixVerse and fetching generated video..."})
    try:
        video_url = await poll_video_status(token)
        # map local paths to server-accessible URL
        try:
            if video_url and Path(video_url).exists():
                disp = f"/downloads/{Path(video_url).name}"
            else:
                disp = video_url
        except Exception:
            disp = video_url
        j.update({"status": "video_ready", "message": "✅ Video ready to watch", "video_url": disp})
    except Exception as e:
        j.update({"status": "error", "message": "Failed to fetch video", "error": str(e)})


async def upload_job_video(job_id: str):
    if job_id not in jobs:
        return
    j = jobs[job_id]
    video_url = j.get("video_url")
    if not video_url:
        j.update({"status": "error", "message": "No video to upload"})
        return
    j.update({"status": "uploading", "message": "⬇️ Downloading video for upload..."})
    try:
        local_path = await download_video(video_url, job_id)
        j.update({"message": "📤 Uploading to YouTube..."})
        title = j.get("youtube_title") or f"LayoffShield – {j.get('prompt_used','Video')}"
        description = j.get("youtube_description") or build_yt_description(j.get('prompt_used',''))
        tags = j.get("youtube_tags") or ["LayoffShield", "career"]
        yt_url = await upload_to_youtube(local_path, title, description, tags)
        j.update({"status": "done", "message": "🎉 Posted to YouTube!", "youtube_url": yt_url})
        Path(local_path).unlink(missing_ok=True)
    except Exception as e:
        j.update({"status": "error", "message": "Upload failed", "error": str(e)})


def build_yt_description(topic: str) -> str:
    """Build YouTube description following LayoffShield brand guidelines"""
    return f"""🛡️ LayoffShield – Your AI-Powered Career Protection Platform

{topic}

LayoffShield empowers employees to stay career-ready:
✅ AI-powered employment risk assessment and monitoring
✅ Personalized guidance from your AI career advisor
✅ Practice with AI-powered mock interviews tailored to your role
✅ Skill gap analysis and career development resources
✅ Community support and professional connections

🔗 Try LayoffShield free → https://layoffshield.com

📌 LayoffShield is NOT an insurance company. Our platform provides career intelligence, 
readiness tools, and community support. Discretionary financial support, where applicable, 
is provided at LayoffShield's sole discretion and is not guaranteed.

#LayoffShield #CareerReady #AICareerCoach #CareerGrowth #MockInterview #CareerDevelopment #Resilience
"""
