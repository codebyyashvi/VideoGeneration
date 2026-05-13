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


# ── Video Generation ───────────────────────────

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
        # Step 1: Generate prompt with Groq
        update("generating_prompt", "🤖 Generating marketing prompt with Groq...")
        prompt = await generate_video_prompt(req.topic)
        update("generating_prompt", "✅ Prompt ready", prompt_used=prompt)

        # Step 2: Submit to PixVerse
        update("generating_video", "🎬 Submitting to PixVerse for video generation...")
        video_id = await generate_video(
            prompt=prompt,
            duration=req.duration,
            quality=req.quality,
            aspect_ratio=req.aspect_ratio,
            style=req.style,
        )

        # Job now waits for user to 'See Video' to fetch it
        update("waiting_for_user", "🟡 Video submitted — click 'See Video' to open and fetch generated video", prompt_used=prompt)
        # store video generation token so fetch endpoint can use it
        jobs[job_id]["generation_token"] = video_id
    except Exception as e:
        jobs[job_id].update({"status": "error", "message": "Pipeline failed", "error": str(e)})
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
    return f"""🛡️ LayoffShield – Your Career Protection Platform

{topic}

LayoffShield helps employees:
✅ Assess their layoff risk with AI-powered analysis
✅ Get personalized career advice from an AI advisor
✅ Practice with AI mock interviews tailored to their profile
✅ Prepare before AND after a layoff happens

🔗 Try LayoffShield free → https://layoffshield.com

#LayoffShield #CareerSecurity #AICareerCoach #JobProtection #MockInterview #LayoffPreparation
"""
