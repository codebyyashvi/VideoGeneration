"""
Configuration — set these as environment variables or in a .env file
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Groq
    groq_api_key: str = ""

    # PixVerse browser automation
    pixverse_api_key: str = ""
    pixverse_base_url: str = "https://app-api.pixverse.ai/openapi/v2"
    pixverse_web_url: str = "https://app.pixverse.ai"
    pixverse_login_timeout_seconds: int = 900
    pixverse_profile_dir: str = ".pixverse-playwright"
    pixverse_browser_channel: str = "chrome"
    pixverse_headless: bool = False

    # YouTube OAuth (Google Cloud Console)
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/auth/youtube/callback"

    # Token storage
    token_file: str = "youtube_token.json"

    # Downloads temp dir
    download_dir: str = "/tmp/layoffshield_videos"

    class Config:
        env_file = ".env"

settings = Settings()
