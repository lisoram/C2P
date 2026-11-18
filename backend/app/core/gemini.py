"""
Gemini SDK connectivity check.
Uses the cheapest currently-stable Flash-class model: gemini-3.5-flash-lite.
Makes one trivial generate_content call to prove the API key works.
Raises loudly if the key is invalid or the API is unreachable.
"""

from google import genai

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_client: genai.Client | None = None


def get_gemini_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


async def check_gemini() -> None:
    """
    Send a trivial prompt to Gemini and confirm a non-empty response.
    Raises if the API key is wrong or the network is unreachable.
    """
    client = get_gemini_client()

    # Use the async client (client.aio). The sync call blocks the event loop,
    # which starves the other health probes and makes them time out.
    response = await client.aio.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents="Reply with the single word OK and nothing else.",
    )

    text = response.text.strip() if response.text else ""
    if not text:
        raise RuntimeError("Gemini returned an empty response during health check")

    logger.info(
        "Gemini API verified",
        extra={"model": settings.GEMINI_MODEL, "response_preview": text[:20]},
    )
