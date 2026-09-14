from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1.transcribe import router as transcribe_router
from app.config.logging_config import get_logger
from app.core.exceptions import ProviderError, AudioFetchError, InvalidRequestError
from app.docs.router import router as docs_router
import app.providers  # noqa: F401 — import triggers provider registration

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Voice Transcription Service starting up")
    yield
    logger.info("Voice Transcription Service shutting down")


app = FastAPI(
    title="Voice Transcription Service",
    lifespan=lifespan,
    docs_url="/swagger",
    redoc_url="/redoc",
)

app.include_router(transcribe_router)
app.include_router(docs_router)

@app.exception_handler(ProviderError)
async def provider_error_handler(request, exc: ProviderError):
    logger.error(
        "ProviderError — provider=%s code=%s message=%s status=%d",
        exc.provider, exc.code, exc.message, exc.status_code,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"provider": exc.provider, "code": exc.code, "message": exc.message},
    )

@app.exception_handler(AudioFetchError)
async def audio_fetch_error_handler(request, exc: AudioFetchError):
    logger.warning("AudioFetchError — %s", exc)
    return JSONResponse(
        status_code=422,
        content={"code": "audio_fetch_error", "message": str(exc)},
    )

@app.exception_handler(InvalidRequestError)
async def invalid_request_error_handler(request, exc: InvalidRequestError):
    logger.warning("InvalidRequestError — %s", exc)
    return JSONResponse(
        status_code=400,
        content={"code": "invalid_request", "message": str(exc)},
    )

@app.get("/health")
async def health():
    logger.debug("Health check requested")
    return {"status": "ok"}