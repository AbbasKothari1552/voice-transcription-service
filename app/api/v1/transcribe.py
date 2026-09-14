import json
import time

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.config.logging_config import get_logger
from app.core.registry import get_provider
from app.core.schemas import TranscriptionResult
from app.core.exceptions import ProviderError, AudioFetchError, InvalidRequestError
from app.core.audio_fetcher import fetch_audio_from_url

logger = get_logger(__name__)

router = APIRouter()

@router.post("/v1/transcribe", response_model=TranscriptionResult)
async def transcribe(
    provider: str = Form(...),
    model: str = Form(...),
    api_key: str = Form(...),
    options: str = Form("{}"),
    file: UploadFile | None = File(None),
    audio_url: str | None = Form(None),
):
    request_start = time.perf_counter()
    logger.info(
        "Transcription request received — provider=%s model=%s audio_source=%s",
        provider, model, "file" if file else "url",
    )

    # --- 1. Validate exactly one audio source was given ---
    if file is None and not audio_url:
        logger.warning("Request rejected: neither 'file' nor 'audio_url' provided")
        raise HTTPException(400, "Provide either 'file' or 'audio_url', got neither.")
    if file is not None and audio_url:
        logger.warning("Request rejected: both 'file' and 'audio_url' provided")
        raise HTTPException(400, "Provide either 'file' or 'audio_url', not both.")

    # --- 2. Parse options safely ---
    try:
        parsed_options = json.loads(options)
        logger.debug("Parsed options: %s", parsed_options)
    except json.JSONDecodeError:
        logger.warning("Request rejected: malformed JSON in 'options' field")
        raise HTTPException(400, "`options` must be valid JSON.")

    # --- 3. Resolve provider + model before touching audio (fail fast) ---
    try:
        provider_impl = get_provider(provider)
    except ValueError as e:
        logger.error("Unknown provider requested: %s", provider)
        raise HTTPException(400, str(e))

    if not provider_impl.validate_model(model):
        logger.error("Invalid model '%s' for provider '%s'", model, provider)
        raise HTTPException(400, f"Model '{model}' is not valid for provider '{provider}'.")

    logger.debug("Provider resolved: %s (model=%s)", provider, model)

    # --- 4. Normalize audio source to bytes, regardless of input type ---
    try:
        if file is not None:
            file_bytes = await file.read()
            file_name = file.filename or "uploaded_audio"
            logger.info(
                "Audio from file upload — name=%s size=%d bytes",
                file_name, len(file_bytes),
            )
        else:
            file_bytes, file_name = await fetch_audio_from_url(audio_url)
            logger.info(
                "Audio fetched from URL — name=%s size=%d bytes",
                file_name, len(file_bytes),
            )
    except AudioFetchError as e:
        logger.error("Audio fetch failed for URL %s — %s", audio_url, e)
        raise HTTPException(422, f"Could not fetch audio_url: {str(e)}")

    if not file_bytes:
        logger.warning("Audio payload is empty — rejecting request")
        raise HTTPException(422, "Audio payload is empty.")

    # --- 5. Delegate to provider ---
    try:
        logger.debug("Sending audio to provider '%s' for transcription", provider)
        result = await provider_impl.transcribe(
            file_bytes=file_bytes,
            file_name=file_name,
            model=model,
            api_key=api_key,
            options=parsed_options,
        )
        elapsed = time.perf_counter() - request_start
        logger.info(
            "Transcription succeeded — provider=%s model=%s duration=%.2fs transcript_length=%d",
            provider, model, elapsed, len(result.transcript),
        )
        return result
    except ProviderError as e:
        elapsed = time.perf_counter() - request_start
        logger.error(
            "Transcription failed — provider=%s code=%s message=%s duration=%.2fs",
            e.provider, e.code, e.message, elapsed,
        )
        raise HTTPException(e.status_code, {"provider": e.provider, "code": e.code, "message": e.message})