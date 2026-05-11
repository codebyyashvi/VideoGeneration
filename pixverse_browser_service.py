"""
PixVerse Service — browser automation using Playwright.

This keeps a persistent PixVerse browser profile so the user can sign in once
through the web UI, then reuse that session for later generations.
"""
from __future__ import annotations

import asyncio
import sys
import re
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import httpx

from config import settings

# Windows event loop fix for Playwright subprocess support
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

try:
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError
    from playwright.async_api import async_playwright
except ImportError as exc:  # pragma: no cover - dependency issue is surfaced at runtime
    async_playwright = None
    PlaywrightTimeoutError = Exception
    _PLAYWRIGHT_IMPORT_ERROR = exc
else:
    _PLAYWRIGHT_IMPORT_ERROR = None

ALLOWED_QUALITIES = {"360p", "540p", "720p"}
MAX_WAIT_SECONDS = 900
POLL_INTERVAL = 5
PIXVERSE_HOME_URL = "https://app.pixverse.ai/"
PIXVERSE_LOGIN_URL = "https://app.pixverse.ai/login"


@dataclass
class _PixVerseSession:
    playwright: object
    context: object
    page: object


_session: Optional[_PixVerseSession] = None
_session_lock = asyncio.Lock()
_generation_state: dict[str, dict[str, str]] = {}


async def _count_locator(locator) -> int:
    try:
        return await locator.count()
    except Exception:
        return 0


async def _click_first_visible_thumbnail(page) -> bool:
    """Attempt to click the first visible thumbnail of the newly generated video."""
    try:
        # Strategy 1: Click on the video card in the grid (most likely structure based on PixVerse UI)
        # Videos are displayed in a grid with large clickable cards
        grid_selectors = [
            'div[class*="grid"] > div:has(img)',  # Grid items with images
            '[class*="gallery"] > div',  # Gallery container items
            'div[role="link"]',  # Role-based interactive divs
            '[class*="video-item"]',  # Video item containers
            '[class*="card"]',  # Generic card containers
        ]
        
        for selector in grid_selectors:
            try:
                items = page.locator(selector)
                count = await items.count()
                if count > 0:
                    for index in range(count):
                        item = items.nth(index)
                        try:
                            box = await item.bounding_box()
                        except Exception:
                            continue
                        
                        if not box:
                            continue
                        # Skip very small items and header area
                        if box["width"] < 100 or box["height"] < 100:
                            continue
                        if box["y"] < 150:  # Skip header area
                            continue
                        
                        # Try to scroll into view and click
                        try:
                            await item.scroll_into_view_if_needed()
                            await asyncio.sleep(0.5)
                        except Exception:
                            pass
                        
                        await item.click(force=True, timeout=5000)
                        return True
            except Exception:
                continue

        # Strategy 2: Try image selectors as fallback
        img_selectors = [
            'img[src*="pixverse"][src*="frame"]',
            'img[src*="media"]',
        ]
        
        for selector in img_selectors:
            try:
                thumbnails = page.locator(selector)
                count = await thumbnails.count()
                if count > 0:
                    for index in range(count):
                        thumb = thumbnails.nth(index)
                        try:
                            box = await thumb.bounding_box()
                        except Exception:
                            continue

                        if not box:
                            continue
                        if box["width"] < 80 or box["height"] < 60:
                            continue
                        if box["y"] < 100:
                            continue

                        # Click on parent or the image itself
                        try:
                            parent = thumb.locator('..')
                            await parent.click(force=True, timeout=5000)
                            return True
                        except Exception:
                            await thumb.click(force=True, timeout=5000)
                            return True
            except Exception:
                continue

        # Strategy 3: Try clicking first visible large element below header
        try:
            all_divs = page.locator('div')
            count = await all_divs.count()
            for index in range(count):
                div = all_divs.nth(index)
                try:
                    box = await div.bounding_box()
                except Exception:
                    continue
                
                if not box:
                    continue
                # Look for large, clickable elements below header
                if box["width"] >= 150 and box["height"] >= 150 and box["y"] > 150:
                    try:
                        await div.click(force=True, timeout=5000)
                        return True
                    except Exception:
                        continue
        except Exception:
            pass

    except Exception:
        pass

    return False


def _download_target(job_id: str) -> Path:
    download_dir = Path(settings.download_dir)
    download_dir.mkdir(parents=True, exist_ok=True)
    return download_dir / f"{job_id}.mp4"


async def _get_session() -> _PixVerseSession:
    if _PLAYWRIGHT_IMPORT_ERROR:
        raise RuntimeError(
            "Playwright is not installed. Run `pip install -r requirements.txt` and `python -m playwright install chromium`."
        ) from _PLAYWRIGHT_IMPORT_ERROR

    global _session
    async with _session_lock:
        if _session is not None:
            return _session

        profile_dir = Path(settings.pixverse_profile_dir)
        profile_dir.mkdir(parents=True, exist_ok=True)

        playwright = await async_playwright().start()
        launch_kwargs = {
            "user_data_dir": str(profile_dir),
            "headless": settings.pixverse_headless,
            "viewport": {"width": 1440, "height": 900},
            "args": ["--start-maximized", "--disable-blink-features=AutomationControlled"],
        }

        browser_channel = getattr(settings, "pixverse_browser_channel", "chrome").strip()
        if browser_channel:
            launch_kwargs["channel"] = browser_channel

        try:
            context = await playwright.chromium.launch_persistent_context(**launch_kwargs)
        except Exception as exc:
            if browser_channel:
                launch_kwargs.pop("channel", None)
                context = await playwright.chromium.launch_persistent_context(**launch_kwargs)
            else:
                raise RuntimeError(
                    f"Failed to start PixVerse browser session using channel '{browser_channel or 'bundled chromium'}'."
                ) from exc

        page = context.pages[0] if context.pages else await context.new_page()
        page.set_default_timeout(30_000)
        _session = _PixVerseSession(playwright=playwright, context=context, page=page)
        return _session


async def _creator_ready(page) -> bool:
    try:
        return await page.get_by_role(
            "textbox", name=re.compile("Describe the content you want to create", re.I)
        ).count() > 0
    except Exception:
        return False


async def _login_confirmed(page) -> bool:
    try:
        login_controls = [
            page.get_by_role("button", name=re.compile("^Login$", re.I)),
            page.get_by_role("button", name=re.compile("Sign in with Google", re.I)),
        ]
        for control in login_controls:
            if await control.count() > 0:
                return False
        return True
    except Exception:
        return False


async def _wait_for_creator(page, timeout_seconds: int) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if await _creator_ready(page):
            return
        await asyncio.sleep(2)
    raise TimeoutError(
        "PixVerse login/session was not ready in time. Sign in in the opened browser window and try again."
    )


async def _ensure_logged_in(page) -> None:
    await page.goto(PIXVERSE_HOME_URL, wait_until="domcontentloaded")
    await page.wait_for_timeout(5000)
    if await _creator_ready(page):
        return

    await page.goto(PIXVERSE_LOGIN_URL, wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)

    try:
        google_button = page.get_by_role("button", name=re.compile("Sign in with Google", re.I))
        if await google_button.count() > 0:
            await google_button.first.click()
    except Exception:
        pass

    await _wait_for_creator(page, getattr(settings, "pixverse_login_timeout_seconds", 900))
    if not await _login_confirmed(page):
        raise RuntimeError(
            "PixVerse sign-in was not confirmed. Please sign in manually in the Chrome window and try again."
        )


async def _best_effort_set_controls(page, duration: int, quality: str, aspect_ratio: str, style: Optional[str]) -> None:
    desired_combo = f"{quality.upper()} {aspect_ratio} {duration}s"
    try:
        combo_button = page.get_by_role("button", name=re.compile(r"\b(360P|540P|720P)\b.*\b\d+s\b", re.I))
        if await combo_button.count() > 0:
            current_label = (await combo_button.first.inner_text()).strip().upper()
            if current_label and current_label != desired_combo.upper():
                await combo_button.first.click()
                await asyncio.sleep(0.5)
                for label in (quality.upper(), aspect_ratio, f"{duration}s"):
                    option = page.get_by_role("button", name=re.compile(re.escape(label), re.I))
                    if await option.count() > 0:
                        await option.first.click()
                        await asyncio.sleep(0.4)
    except Exception:
        pass

    if style:
        try:
            style_button = page.get_by_role("button", name=re.compile("Style|Template|Cinematic|Realistic|Anime|3D", re.I))
            if await style_button.count() > 0:
                await style_button.first.click()
                await asyncio.sleep(0.3)
                option = page.get_by_role("button", name=re.compile(re.escape(style.replace("_", " ")), re.I))
                if await option.count() > 0:
                    await option.first.click()
        except Exception:
            pass


async def _click_first_grid_video(page) -> bool:
    """Aggressively try to click the first video card in the grid."""
    try:
        # First, make sure we're looking at the Created tab results
        # Try clicking the video card by targeting the first large img element in the grid
        all_imgs = page.locator('img')
        img_count = await all_imgs.count()
        
        for i in range(img_count):
            img = all_imgs.nth(i)
            try:
                box = await img.bounding_box()
                if not box:
                    continue
                    
                # Skip header/navigation images (small images in top area)
                if box["y"] < 150 or box["width"] < 100:
                    continue
                
                # Found a large image in the main content area
                # Try to click on it or its parent
                try:
                    # Try clicking the image's parent container
                    await img.click(force=True, timeout=3000)
                    return True
                except Exception:
                    # Try parent of parent
                    try:
                        parent = page.locator(f'img >> nth={i}').locator('..')
                        await parent.click(force=True, timeout=3000)
                        return True
                    except Exception:
                        pass
            except Exception:
                continue
    except Exception:
        pass
    
    return False


async def _wait_for_result_download(page, job_id: str) -> str:
    deadline = time.monotonic() + MAX_WAIT_SECONDS
    target_path = _download_target(job_id)
    state = _generation_state.get(job_id, {})
    baseline_video_count = int(state.get("baseline_video_count", "0"))
    baseline_download_count = int(state.get("baseline_download_count", "0"))
    baseline_thumbnail_count = int(state.get("baseline_thumbnail_count", "0"))
    
    poll_count = 0

    while time.monotonic() < deadline:
        poll_count += 1
        
        # Try to click newly generated video thumbnail using multiple strategies
        try:
            img_selectors = [
                'img[src*="pixverse%2Fvideo%2Fframe"]',
                'img[src*="media.pixverse.ai/pixverse%2Fvideo%2Fframe"]',
                'img[src*="pixverse"][src*="frame"]',
            ]
            
            thumbnail_count = 0
            for selector in img_selectors:
                count = await _count_locator(page.locator(selector))
                thumbnail_count = max(thumbnail_count, count)
            
            if thumbnail_count > baseline_thumbnail_count:
                # Strategy 1: Try specific thumbnail click
                if await _click_first_visible_thumbnail(page):
                    await page.wait_for_timeout(2500)
                else:
                    # Strategy 2: If specific selector failed, try aggressive grid click
                    if await _click_first_grid_video(page):
                        await page.wait_for_timeout(2500)
        except Exception:
            pass

        # Look for video element (appears after thumbnail click)
        try:
            current_video_count = await _count_locator(page.locator("video"))
            if current_video_count > baseline_video_count:
                video = page.locator("video").nth(current_video_count - 1)
                src = await video.get_attribute("src")
                if src:
                    if src.startswith("blob:"):
                        blob_bytes = await page.evaluate(
                            """
                            async (blobUrl) => {
                                const response = await fetch(blobUrl);
                                const buffer = await response.arrayBuffer();
                                return Array.from(new Uint8Array(buffer));
                            }
                            """,
                            src,
                        )
                        target_path.write_bytes(bytes(blob_bytes))
                        return str(target_path)
                    return src
        except Exception:
            pass

        # Look for download button (may appear after detail panel opens)
        try:
            download_candidates = [
                page.get_by_role("button", name=re.compile("Download", re.I)),
                page.get_by_role("link", name=re.compile("Download", re.I)),
                page.locator('a[download]'),
            ]
            for candidate in download_candidates:
                current_download_count = await _count_locator(candidate)
                if current_download_count <= baseline_download_count:
                    continue
                try:
                    async with page.expect_download(timeout=10_000) as download_info:
                        await candidate.first.click()
                    download = await download_info.value
                    await download.save_as(str(target_path))
                    return str(target_path)
                except PlaywrightTimeoutError:
                    href = await candidate.first.get_attribute("href")
                    if href:
                        return href
                except Exception:
                    href = await candidate.first.get_attribute("href")
                    if href:
                        return href
        except Exception:
            pass

        await asyncio.sleep(POLL_INTERVAL)

    raise TimeoutError(f"PixVerse generation timed out after {MAX_WAIT_SECONDS}s")


async def generate_video(
    prompt: str,
    duration: int = 5,
    quality: str = "720p",
    aspect_ratio: str = "16:9",
    style: str | None = None,
    motion_mode: str = "normal",
) -> str:
    """Submit a prompt in the PixVerse web UI and return a generation token."""
    if quality not in ALLOWED_QUALITIES:
        raise ValueError(f"Quality must be one of {ALLOWED_QUALITIES} on free tier")

    session = await _get_session()
    page = session.page
    await _ensure_logged_in(page)
    await page.goto(PIXVERSE_HOME_URL, wait_until="domcontentloaded")
    await page.wait_for_timeout(5000)
    await _wait_for_creator(page, 120)
    if not await _login_confirmed(page):
        raise RuntimeError(
            "PixVerse sign-in was not confirmed. Please sign in manually in the Chrome window and try again."
        )

    baseline_video_count = await _count_locator(page.locator("video"))
    baseline_download_count = await _count_locator(page.locator('a[download]'))
    baseline_thumbnail_count = await _count_locator(
        page.locator('img[src*="pixverse%2Fvideo%2Fframe"], img[src*="media.pixverse.ai/pixverse%2Fvideo%2Fframe"]')
    )

    prompt_box = page.get_by_role(
        "textbox", name=re.compile("Describe the content you want to create", re.I)
    )
    await prompt_box.first.fill(prompt)
    await _best_effort_set_controls(page, duration, quality, aspect_ratio, style)

    generation_id = str(uuid.uuid4())
    _generation_state[generation_id] = {
        "prompt": prompt,
        "duration": str(duration),
        "quality": quality,
        "aspect_ratio": aspect_ratio,
        "baseline_video_count": str(baseline_video_count),
        "baseline_download_count": str(baseline_download_count),
        "baseline_thumbnail_count": str(baseline_thumbnail_count),
    }

    create_button = page.get_by_role("button", name=re.compile(r"Create", re.I))
    if await create_button.count() == 0:
        raise RuntimeError("Could not find PixVerse Create button in the web UI")

    await create_button.first.click()
    
    # Wait for progress indicator to appear and stabilize
    await page.wait_for_timeout(3000)
    
    return generation_id


async def poll_video_status(video_id: str) -> str:
    """Wait for PixVerse to finish and return a downloadable video location."""
    if video_id not in _generation_state:
        raise RuntimeError("Unknown PixVerse generation token")

    session = await _get_session()
    page = session.page
    return await _wait_for_result_download(page, video_id)


async def download_video(url: str, job_id: str) -> str:
    """Download the generated video to local disk if the result is a remote URL."""
    if not url:
        raise ValueError("Missing PixVerse video URL or local path")

    candidate_path = Path(url.replace("file://", "")) if url.startswith("file://") else Path(url)
    if candidate_path.exists():
        return str(candidate_path)

    download_path = _download_target(job_id)
    async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            with open(download_path, "wb") as file_handle:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    file_handle.write(chunk)

    return str(download_path)
