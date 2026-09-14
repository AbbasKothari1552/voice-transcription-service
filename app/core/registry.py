from app.config.logging_config import get_logger
from app.core.base_provider import BaseTranscriptionProvider

logger = get_logger(__name__)

_REGISTRY: dict[str, BaseTranscriptionProvider] = {}

def register_provider(provider: BaseTranscriptionProvider):
    _REGISTRY[provider.name] = provider
    logger.info("Registered transcription provider: %s", provider.name)

def get_provider(name: str) -> BaseTranscriptionProvider:
    if name not in _REGISTRY:
        logger.warning(
            "Provider '%s' not found — registered providers: %s",
            name, list(_REGISTRY.keys()),
        )
        raise ValueError(f"Unknown provider: {name}")
    logger.debug("Provider lookup: %s", name)
    return _REGISTRY[name]

def list_providers() -> list[str]:
    providers = list(_REGISTRY.keys())
    logger.debug("Listing providers: %s", providers)
    return providers