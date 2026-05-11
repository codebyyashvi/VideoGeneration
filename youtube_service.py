"""
YouTube Service — OAuth 2.0 (one-time auth) + video upload
Uses google-auth + googleapiclient libraries
"""
import json
import asyncio
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from config import settings

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

# Store OAuth flow temporarily (in-memory; fine for single-user setup)
_active_flow: Optional[Flow] = None


def _get_client_config() -> dict:
    return {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uris": [settings.google_redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def get_oauth_url() -> str:
    """Create OAuth flow and return authorization URL."""
    global _active_flow
    _active_flow = Flow.from_client_config(
        _get_client_config(),
        scopes=SCOPES,
        redirect_uri=settings.google_redirect_uri,
    )
    auth_url, _ = _active_flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return auth_url


def handle_oauth_callback(code: str) -> bool:
    """Exchange auth code for tokens and save to disk."""
    global _active_flow
    if not _active_flow:
        return False

    try:
        _active_flow.fetch_token(code=code)
        creds = _active_flow.credentials
        _save_credentials(creds)
        _active_flow = None
        return True
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return False


def is_authenticated() -> bool:
    """Check if valid YouTube credentials exist."""
    creds = _load_credentials()
    return creds is not None and creds.valid


def _load_credentials() -> Optional[Credentials]:
    token_path = Path(settings.token_file)
    if not token_path.exists():
        return None

    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_credentials(creds)
        except Exception:
            return None

    return creds if creds and creds.valid else None


def _save_credentials(creds: Credentials):
    token_path = Path(settings.token_file)
    with open(token_path, "w") as f:
        f.write(creds.to_json())


async def upload_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list[str],
    category_id: str = "22",      # People & Blogs; 28 = Science & Technology
    privacy_status: str = "public",
) -> str:
    """
    Upload a video to YouTube.
    Returns the YouTube video URL.
    Runs sync Google API call in executor to avoid blocking the event loop.
    """
    creds = _load_credentials()
    if not creds:
        raise RuntimeError("YouTube not authenticated. Visit /auth/youtube first.")

    def _upload():
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": title[:100],          # YouTube max 100 chars
                "description": description[:5000],
                "tags": tags[:500],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024 * 1024 * 5,  # 5 MB chunks
        )

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"  Upload progress: {pct}%")

        video_id = response["id"]
        return f"https://www.youtube.com/watch?v={video_id}"

    # Run blocking upload in thread pool
    loop = asyncio.get_event_loop()
    yt_url = await loop.run_in_executor(None, _upload)
    return yt_url
