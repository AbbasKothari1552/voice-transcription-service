class ProviderError(Exception):
    """Normalized error shape across all provider SDK exceptions."""
    def __init__(self, provider: str, code: str, message: str, status_code: int = 502):
        self.provider = provider
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{provider}] {code}: {message}")

class UnsupportedModelError(Exception):
    pass

class AudioFetchError(Exception):
    """Raised when downloading audio from a URL fails or fails validation."""
    pass

class InvalidRequestError(Exception):
    """Raised for malformed requests (e.g. both file and url given, or neither)."""
    pass