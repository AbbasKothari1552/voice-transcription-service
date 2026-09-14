from abc import ABC, abstractmethod
from app.core.schemas import TranscriptionResult

class BaseTranscriptionProvider(ABC):
    name: str

    @abstractmethod
    def validate_model(self, model: str) -> bool:
        ...

    @abstractmethod
    async def transcribe(
        self,
        *,
        file_bytes: bytes,
        file_name: str,
        model: str,
        api_key: str,
        options: dict,
    ) -> TranscriptionResult:
        ...