"""
Qdrant client wrapper.
check_qdrant() connects and ensures the 'drawings' collection exists.
If it doesn't exist yet, it is created with the configured vector size.
Raises loudly if Qdrant is unreachable.
"""

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_client: AsyncQdrantClient | None = None


def get_qdrant_client() -> AsyncQdrantClient:
    global _client
    if _client is None:
        _client = AsyncQdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            timeout=2.0,
        )
    return _client


async def check_qdrant() -> None:
    """
    Connect to Qdrant and ensure the target collection exists.
    Creates it (empty) if it does not exist yet.
    Raises if Qdrant is unreachable.
    """
    client = get_qdrant_client()

    # Verify connectivity with a lightweight info call
    await client.get_collections()

    collection = settings.QDRANT_COLLECTION
    try:
        await client.get_collection(collection)
        logger.info("Qdrant collection already exists", extra={"collection": collection})
    except (UnexpectedResponse, Exception) as exc:
        # Collection does not exist — create it
        if "not found" in str(exc).lower() or "404" in str(exc):
            await client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(
                    size=settings.QDRANT_VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(
                "Qdrant collection created",
                extra={"collection": collection, "vector_size": settings.QDRANT_VECTOR_SIZE},
            )
        else:
            raise

    logger.info("Qdrant connection verified")
