from pydantic import BaseModel, model_validator
from typing import Optional, Any

class TranscriptionResult(BaseModel):
    transcript: str
    language_code: Optional[str] = None
    raw_provider_response: Optional[dict] = None

class TranscriptionRequestMeta(BaseModel):
    """Everything except the audio itself — parsed from form fields."""
    provider: str
    model: str
    api_key: str
    audio_url: Optional[str] = None
    options: dict[str, Any] = {}

    @model_validator(mode="after")
    def check_source_exclusivity(self):
        # file presence is checked separately in the route handler,
        # since UploadFile isn't part of this model. This validator
        # just ensures audio_url, if given, looks sane.
        if self.audio_url is not None and not self.audio_url.strip():
            raise ValueError("audio_url cannot be empty string")
        return self