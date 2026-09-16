import asyncio
import json
import os
import tempfile
import time
from pathlib import Path

from sarvamai import SarvamAI
from sarvamai.core.api_error import ApiError

from app.config.logging_config import get_logger
from app.core.base_provider import BaseTranscriptionProvider
from app.core.schemas import TranscriptionResult
from app.core.exceptions import ProviderError
from app.providers.sarvam.config import (
    VALID_MODELS,
    SAARAS_MODELS,
    BATCH_POLL_INTERVAL_SECONDS,
    BATCH_TIMEOUT_SECONDS,
)

logger = get_logger(__name__)

# Fragments Sarvam uses in the 422 error body when audio exceeds the
# REST endpoint's 30-second cap. The HTTP status/code alone (422 /
# unprocessable_entity_error) is shared with other validation failures
# (bad format, corrupt file), so we sniff the message too before deciding
# this is a "too long, retry via Batch" situation rather than a real
# validation error we should just surface to the caller.
_DURATION_ERROR_HINTS = ("30 second", "duration", "too long", "exceeds")


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
        """
        Transcribe via Sarvam. Tries the fast synchronous REST endpoint first
        (<=30s audio). If Sarvam rejects the audio for being too long, we
        transparently fall back to the Batch Job API, which supports audio
        up to 2 hours. Callers don't need to know or care which path ran —
        they get back the same TranscriptionResult either way.
        """
        try:
            return await self._transcribe_rest(
                file_bytes=file_bytes,
                file_name=file_name,
                model=model,
                api_key=api_key,
                options=options,
            )
        except ApiError as e:
            if self._is_duration_limit_error(e):
                logger.info(
                    "Sarvam REST endpoint rejected audio as too long (model=%s, "
                    "file=%s) — falling back to Batch API",
                    model, file_name,
                )
                return await self._transcribe_batch(
                    file_bytes=file_bytes,
                    file_name=file_name,
                    model=model,
                    api_key=api_key,
                    options=options,
                )
            logger.error("Sarvam API call failed — model=%s error=%s", model, e)
            raise ProviderError(
                provider=self.name,
                code="transcription_failed",
                message=str(e),
            ) from e
        except Exception as e:
            logger.error("Sarvam API call failed — model=%s error=%s", model, e)
            raise ProviderError(
                provider=self.name,
                code="transcription_failed",
                message=str(e),
            ) from e

    @staticmethod
    def _is_duration_limit_error(e: ApiError) -> bool:
        # Sarvam has returned this as both 400 (invalid_request_error) and
        # 422 (unprocessable_entity_error) depending on model/endpoint
        # version, so we don't gate on status code alone — the message
        # text is the reliable signal.
        if getattr(e, "status_code", None) not in (400, 422):
            return False
        body_text = str(getattr(e, "body", "") or "").lower()
        return any(hint in body_text for hint in _DURATION_ERROR_HINTS)

    def _build_common_options(self, model: str, options: dict) -> dict:
        """Options shared between the REST and Batch code paths."""
        kwargs = {}
        if options.get("language_code"):
            kwargs["language_code"] = options["language_code"]
        if "with_timestamps" in options:
            kwargs["with_timestamps"] = options["with_timestamps"]
        # `mode` is only valid for saaras:* models
        if model in SAARAS_MODELS and options.get("mode"):
            kwargs["mode"] = options["mode"]
        return kwargs

    # ------------------------------------------------------------------
    # REST path (<=30s audio) — original synchronous transcription call
    # ------------------------------------------------------------------
    async def _transcribe_rest(self, *, file_bytes, file_name, model, api_key, options):
        logger.info(
            "Sarvam REST transcription starting — model=%s file=%s size=%d bytes",
            model, file_name, len(file_bytes),
        )
        client = SarvamAI(api_subscription_key=api_key)

        kwargs = {
            "file": (file_name, file_bytes),
            "model": model,
            "mode": "translit",
            **self._build_common_options(model, options),
        }
        if kwargs.get("language_code"):
            logger.debug("Sarvam: using language_code=%s", kwargs["language_code"])
        if "with_timestamps" in kwargs:
            logger.debug("Sarvam: with_timestamps=%s", kwargs["with_timestamps"])
        if kwargs.get("mode"):
            logger.debug("Sarvam: saaras mode=%s", kwargs["mode"])

        logger.debug("Offloading Sarvam SDK call to thread pool")
        start = time.perf_counter()
        result = await asyncio.to_thread(client.speech_to_text.transcribe, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(
            "Sarvam REST API call succeeded — model=%s duration=%.2fs",
            model, elapsed,
        )

        raw = result.model_dump() if hasattr(result, "model_dump") else {"transcript": result.transcript}
        logger.debug("Sarvam transcript preview: %.100s...", result.transcript)

        return TranscriptionResult(
            transcript=result.transcript,
            language_code=getattr(result, "language_code", None),
            raw_provider_response=raw,
        )

    # ------------------------------------------------------------------
    # Batch path (>30s audio, up to 2 hours) — async job workflow
    # ------------------------------------------------------------------
    async def _transcribe_batch(self, *, file_bytes, file_name, model, api_key, options):
        logger.info(
            "Sarvam Batch transcription starting — model=%s file=%s size=%d bytes",
            model, file_name, len(file_bytes),
        )
        client = SarvamAI(api_subscription_key=api_key)
        job_kwargs = {
            "model": model,
            **self._build_common_options(model, options),
        }
        if "with_diarization" in options:
            job_kwargs["with_diarization"] = options["with_diarization"]
        if options.get("num_speakers"):
            job_kwargs["num_speakers"] = options["num_speakers"]

        suffix = Path(file_name).suffix or ".wav"

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                # job.upload_files() needs a real path on disk, not bytes,
                # so we stage the file locally for the duration of the job.
                input_path = os.path.join(tmp_dir, f"input{suffix}")
                with open(input_path, "wb") as f:
                    f.write(file_bytes)

                output_dir = os.path.join(tmp_dir, "output")
                os.makedirs(output_dir, exist_ok=True)

                start = time.perf_counter()
                job = await asyncio.to_thread(
                    self._run_batch_job_sync,
                    client, input_path, output_dir, job_kwargs,
                )
                elapsed = time.perf_counter() - start
                logger.info(
                    "Sarvam Batch job completed — model=%s duration=%.2fs",
                    model, elapsed,
                )

                failed = getattr(job, "failed_files_count", 0) or 0
                if failed:
                    error_message = getattr(job, "error_message", None) or "Batch job reported failed files"
                    raise ProviderError(
                        provider=self.name,
                        code="batch_transcription_failed",
                        message=error_message,
                    )

                return self._parse_batch_output(output_dir)

        except ProviderError:
            raise
        except Exception as e:
            logger.error("Sarvam Batch API call failed — model=%s error=%s", model, e)
            raise ProviderError(
                provider=self.name,
                code="batch_transcription_failed",
                message=str(e),
            ) from e

    @staticmethod
    def _run_batch_job_sync(client: SarvamAI, input_path: str, output_dir: str, job_kwargs: dict):
        """
        Runs the full blocking Batch job lifecycle in one thread-pool call
        (create -> upload -> start -> poll -> download) so we only pay for
        one asyncio.to_thread hop instead of five.
        """
        job = client.speech_to_text_job.create_job(**job_kwargs)
        job.upload_files(file_paths=[input_path])
        job.start()
        job.wait_until_complete(
            poll_interval=BATCH_POLL_INTERVAL_SECONDS,
            timeout=BATCH_TIMEOUT_SECONDS,
        )
        job.download_outputs(output_dir=output_dir)
        return job

    @staticmethod
    def _parse_batch_output(output_dir: str) -> TranscriptionResult:
        """
        Reads the single output JSON file the Batch API writes for our one
        uploaded file (e.g. "0.json") and normalizes it into the same
        TranscriptionResult shape the REST path returns.
        """
        output_files = sorted(
            f for f in os.listdir(output_dir) if f.endswith(".json")
        )
        if not output_files:
            raise ProviderError(
                provider="sarvam",
                code="batch_transcription_failed",
                message="Batch job completed but produced no output file",
            )

        with open(os.path.join(output_dir, output_files[0]), "r", encoding="utf-8") as f:
            raw = json.load(f)

        # Plain transcription modes return {"transcript": ...}.
        # Diarized jobs return {"diarized_transcript": {"entries": [...]}}
        # instead — stitch those entries into a single readable transcript
        # while keeping the full structured data in raw_provider_response.
        transcript = raw.get("transcript")
        if not transcript and "diarized_transcript" in raw:
            entries = raw["diarized_transcript"].get("entries", [])
            transcript = " ".join(
                entry.get("transcript", "") for entry in entries
            ).strip()

        return TranscriptionResult(
            transcript=transcript or "",
            language_code=raw.get("language_code"),
            raw_provider_response=raw,
        )