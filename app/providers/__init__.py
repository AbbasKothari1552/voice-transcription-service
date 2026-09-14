from app.config.logging_config import get_logger
from app.core.registry import register_provider
from app.providers.groq.provider import GroqProvider
from app.providers.sarvam.provider import SarvamProvider

logger = get_logger(__name__)

logger.info("Loading transcription providers...")
register_provider(GroqProvider())
register_provider(SarvamProvider())
logger.info("All providers registered successfully")