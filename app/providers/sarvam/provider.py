import asyncio
import time

from sarvamai import SarvamAI

from app.config.logging_config import get_logger
from app.core.base_provider import BaseTranscriptionProvider
from app.core.schemas import TranscriptionResult
from app.core.exceptions import ProviderError
from app.providers.sarvam.config import VALID_MODELS, SAARAS_MODELS

logger = get_logger(__name__)


class SarvamProvider(BaseTranscriptionProvider):
    name = "sarvam"

    def validate_model(self, model: str) -> bool:
        is_valid = model in VALID_MODELS
        if not is_valid:
            logger.debug(
                "Sarvam model validation failed: '%s' not in %s", model, VALID_MODELS,
            )
        return is_valid

    async def transcribe(self, *, file_bytes, file_name, model, api_key, options):
        logger.info(
            "Sarvam transcription starting — model=%s file=%s size=%d bytes",
            model, file_name, len(file_bytes),
        )
        client = SarvamAI(api_subscription_key=api_key)

        kwargs = {
            "file": (file_name, file_bytes),
            "model": model,
        }

        # Optional parameters — only send if explicitly provided
        if options.get("language_code"):
            kwargs["language_code"] = options["language_code"]
            logger.debug("Sarvam: using language_code=%s", options["language_code"])
        if "with_timestamps" in options:
            kwargs["with_timestamps"] = options["with_timestamps"]
            logger.debug("Sarvam: with_timestamps=%s", options["with_timestamps"])

        # `mode` param is only valid for saaras:* models
        if model in SAARAS_MODELS and options.get("mode"):
            kwargs["mode"] = options["mode"]
            logger.debug("Sarvam: saaras mode=%s", options["mode"])

        try:
            # SarvamAI SDK is synchronous — offload to a thread to avoid
            # blocking the async event loop.
            logger.debug("Offloading Sarvam SDK call to thread pool")
            start = time.perf_counter()
            result = await asyncio.to_thread(
                client.speech_to_text.transcribe, **kwargs
            )
            elapsed = time.perf_counter() - start
            logger.info(
                "Sarvam API call succeeded — model=%s duration=%.2fs",
                model, elapsed,
            )
        except Exception as e:
            logger.error("Sarvam API call failed — model=%s error=%s", model, e)
            raise ProviderError(
                provider=self.name,
                code="transcription_failed",
                message=str(e),
            ) from e

        # Build raw response dict for debugging / downstream use
        raw = result.model_dump() if hasattr(result, "model_dump") else {"transcript": result.transcript}

        logger.debug(
            "Sarvam transcript preview: %.100s...", result.transcript,
        )

        return TranscriptionResult(
            transcript=result.transcript,
            language_code=getattr(result, "language_code", None),
            raw_provider_response=raw,
        )