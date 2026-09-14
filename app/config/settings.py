from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "voice-transcription-service"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: Path = Path("logs")
    MAX_AUDIO_BYTES: int = 25 * 1024 * 1024
    REQUEST_TIMEOUT_SECONDS: int = 300

    class Config:
        env_file = ".env"


settings = Settings()