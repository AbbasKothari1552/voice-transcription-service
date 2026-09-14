import httpx

from app.config.logging_config import get_logger
from app.core.exceptions import AudioFetchError

logger = get_logger(__name__)

MAX_AUDIO_BYTES = 25 * 1024 * 1024  # 25MB, adjust to your ceiling
ALLOWED_CONTENT_TYPES_PREFIX = ("audio/", "video/")  # some containers report video/*

async def fetch_audio_from_url(url: str) -> tuple[bytes, str]:
    """
    Downloads audio from a URL with size and content-type guardrails.
    Returns (file_bytes, inferred_file_name).
    """
    logger.info("Fetching audio from URL: %s", url)

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                logger.debug("HTTP %d from %s", response.status_code, url)

                content_type = response.headers.get("content-type", "")
                if not content_type.startswith(ALLOWED_CONTENT_TYPES_PREFIX):
                    logger.warning(
                        "Rejected content-type '%s' from URL %s (expected audio/* or video/*)",
                        content_type, url,
                    )
                    raise AudioFetchError(
                        f"URL did not return audio/video content-type, got: {content_type}"
                    )

                logger.debug("Content-Type accepted: %s", content_type)

                chunks = bytearray()
                async for chunk in response.aiter_bytes():
                    chunks.extend(chunk)
                    if len(chunks) > MAX_AUDIO_BYTES:
                        logger.error(
                            "Audio from %s exceeds max size (%d bytes), aborting download",
                            url, MAX_AUDIO_BYTES,
                        )
                        raise AudioFetchError(
                            f"Audio exceeds max allowed size of {MAX_AUDIO_BYTES} bytes"
                        )

        file_name = url.split("/")[-1].split("?")[0] or "downloaded_audio"
        logger.info(
            "Audio download complete — file=%s size=%d bytes",
            file_name, len(chunks),
        )
        return bytes(chunks), file_name

    except httpx.HTTPStatusError as e:
        logger.error("HTTP error fetching %s — status=%d", url, e.response.status_code)
        raise AudioFetchError(f"Failed to fetch URL, status={e.response.status_code}") from e
    except httpx.RequestError as e:
        logger.error("Network error fetching %s — %s", url, e)
        raise AudioFetchError(f"Network error fetching URL: {str(e)}") from e