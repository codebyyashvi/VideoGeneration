"""
PixVerse Service — text-to-video generation using the official PixVerse API
Free tier: up to 720p, 3 concurrent requests, text-to-video supported
API docs: https://docs.platform.pixverse.ai
"""
import uuid
import asyncio
import httpx
from pathlib import Path
from config import settings

# Free tier supports: 360p, 540p, 720p (NOT 1080p)
ALLOWED_QUALITIES = {"360p", "540p", "720p"}
MAX_POLL_SECONDS = 600  # 10 minutes max
POLL_INTERVAL = 5       # seconds between polls

# PixVerse status codes
STATUS_SUCCESS = 1
STATUS_WAITING = 5
STATUS_MODERATION_FAIL = 7
STATUS_FAILED = 8


async def generate_video(
    prompt: str,
    duration: int = 5,
    quality: str = "720p",
    aspect_ratio: str = "16:9",
    style: str | None = None,
    motion_mode: str = "normal",  # "normal" | "fast" (fast uses 2x credits)
) -> int:
    """
    Submit a text-to-video job to PixVerse.
    Returns the video_id for polling.
    
    Free tier caps:
    - Max quality: 720p
    - Max concurrency: 3
    - Duration: 5-10 seconds recommended (longer = more credits)
    """
    if quality not in ALLOWED_QUALITIES:
        raise ValueError(f"Quality must be one of {ALLOWED_QUALITIES} on free tier")

    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
        "model": "v4",           # v3.5 / v4 / v4.5 / v5 — v4 is reliable on free tier
        "quality": quality,
        "motion_mode": motion_mode,
        "water_mark": False,
    }

    if style:
        payload["style"] = style  # realistic | anime | 3d_animation

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{settings.pixverse_base_url}/video/text/generate",
            headers={
                "API-KEY": settings.pixverse_api_key,
                "Ai-trace-id": str(uuid.uuid4()),  # MUST be unique per request
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("ErrCode") != 0:
            raise RuntimeError(f"PixVerse error: {data.get('ErrMsg', 'Unknown error')}")

        video_id = data["Resp"]["video_id"]
        return video_id


async def poll_video_status(video_id: int) -> str:
    """
    Poll PixVerse until the video is ready.
    Returns the download URL.
    
    Status codes:
    1 = Success (done)
    5 = Waiting / processing
    7 = Content moderation failure
    8 = Generation failed
    """
    deadline = asyncio.get_event_loop().time() + MAX_POLL_SECONDS

    async with httpx.AsyncClient(timeout=30) as client:
        while asyncio.get_event_loop().time() < deadline:
            response = await client.get(
                f"{settings.pixverse_base_url}/video/result/{video_id}",
                headers={
                    "API-KEY": settings.pixverse_api_key,
                    "Ai-trace-id": str(uuid.uuid4()),
                },
            )
            response.raise_for_status()
            data = response.json()

            if data.get("ErrCode") != 0:
                raise RuntimeError(f"PixVerse poll error: {data.get('ErrMsg')}")

            resp = data["Resp"]
            status = resp.get("status")

            if status == STATUS_SUCCESS:
                url = resp.get("url")
                if not url:
                    raise RuntimeError("Video ready but no URL returned")
                return url

            elif status == STATUS_MODERATION_FAIL:
                raise RuntimeError("PixVerse rejected prompt (content moderation). Try a different topic.")

            elif status == STATUS_FAILED:
                raise RuntimeError("PixVerse video generation failed.")

            elif status == STATUS_WAITING:
                await asyncio.sleep(POLL_INTERVAL)

            else:
                # Unknown status, keep waiting
                await asyncio.sleep(POLL_INTERVAL)

    raise TimeoutError(f"Video generation timed out after {MAX_POLL_SECONDS}s")


async def download_video(url: str, job_id: str) -> str:
    """Download generated video to local disk. Returns local file path."""
    download_dir = Path(settings.download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)

    local_path = download_dir / f"{job_id}.mp4"

    async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            with open(local_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    f.write(chunk)

    return str(local_path)
