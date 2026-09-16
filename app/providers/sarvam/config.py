VALID_MODELS = {
    "saarika:v1", "saarika:v2", "saarika:v2.5", "saarika:flash",
    "saaras:v3", "saaras:v3-realtime", "saaras:v4", "saaras:v4-multispk",
}

# saaras models accept the `mode` parameter (transcribe, translate, verbatim, etc.)
SAARAS_MODELS = {
    "saaras:v3", "saaras:v3-realtime", "saaras:v4", "saaras:v4-multispk",
}

DEFAULT_MODEL = "saaras:v4"

# --- Batch API settings -----------------------------------------------
# Sarvam's synchronous REST endpoint (speech_to_text.transcribe) hard-caps
# audio at 30 seconds and returns HTTP 422 (`unprocessable_entity_error`)
# for anything longer. There is no parameter to raise that limit — Sarvam's
# own docs say to route longer audio through the Batch Job API instead
# (POST /speech-to-text/job/v1 -> upload -> start -> poll -> download).
# https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api

# How often to poll the job status endpoint (seconds).
BATCH_POLL_INTERVAL_SECONDS = 5

# Give up waiting after this long (seconds). Sarvam's own SDK default is
# 600s (10 min); we give a bit more headroom for large files. Bump this
# if you routinely process very long recordings.
BATCH_TIMEOUT_SECONDS = 1800

# The specific error code Sarvam returns when audio exceeds the REST
# endpoint's 30-second limit. Used to detect when to fall back to Batch.
DURATION_LIMIT_ERROR_CODE = "unprocessable_entity_error"