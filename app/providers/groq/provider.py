import time

from groq import AsyncGroq

from app.config.logging_config import get_logger
from app.core.base_provider import BaseTranscriptionProvider
from app.core.schemas import TranscriptionResult
from app.core.exceptions import ProviderError
from app.providers.groq.config import VALID_MODELS, DEFAULT_RESPONSE_FORMAT

logger = get_logger(__name__)


class GroqProvider(BaseTranscriptionProvider):
    name = "groq"

    def validate_model(self, model: str) -> bool:
        is_valid = model in VALID_MODELS
        if not is_valid:
            logger.debug(
                "Groq model validation failed: '%s' not in %s", model, VALID_MODELS,
            )
        return is_valid

    async def transcribe(self, *, file_bytes, file_name, model, api_key, options):
        logger.info(
            "Groq transcription starting — model=%s file=%s size=%d bytes",
            model, file_name, len(file_bytes),
        )
        client = AsyncGroq(api_key=api_key)

        kwargs = {
            "file": (file_name, file_bytes),
            "model": model,
            "response_format": DEFAULT_RESPONSE_FORMAT,
        }

        # Optional parameters — only send if explicitly provided
        if options.get("language_code"):
            kwargs["language"] = options["language_code"]
            logger.debug("Groq: using language=%s", options["language_code"])
        if options.get("prompt"):
            kwargs["prompt"] = options["prompt"]
            logger.debug("Groq: using custom prompt")

        try:
            start = time.perf_counter()
            result = await client.audio.transcriptions.create(**kwargs)
            elapsed = time.perf_counter() - start
            logger.info(
                "Groq API call succeeded — model=%s duration=%.2fs",
                model, elapsed,
            )
        except Exception as e:
            logger.error("Groq API call failed — model=%s error=%s", model, e)
            raise ProviderError(
                provider=self.name,
                code="transcription_failed",
                message=str(e),
            ) from e

        # Build raw response dict for debugging / downstream use
        raw = result.model_dump() if hasattr(result, "model_dump") else {"text": result.text}

        logger.debug(
            "Groq transcript preview: %.100s...", result.text,
        )

        return TranscriptionResult(
            transcript=result.text,
            language_code=getattr(result, "language", None),
            raw_provider_response=raw,
        )