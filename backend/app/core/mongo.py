"""
MongoDB / GridFS client (Motor – async).
check_mongodb() performs a real round-trip:
  upload a small test file → download it → byte-compare → delete it.
Raises loudly if MongoDB is unreachable or the round-trip fails.
"""

import io

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_client: motor.motor_asyncio.AsyncIOMotorClient | None = None


def get_mongo_client() -> motor.motor_asyncio.AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=2000,
        )
    return _client


def get_db():
    return get_mongo_client()[settings.MONGODB_DB]


async def check_mongodb() -> None:
    """
    Perform a GridFS round-trip:
      1. Upload 16 bytes to GridFS as 'health_check.bin'
      2. Download it back
      3. Assert the bytes match
      4. Delete the uploaded file
    Raises if anything goes wrong.
    """
    client = get_mongo_client()
    db = client[settings.MONGODB_DB]
    bucket = AsyncIOMotorGridFSBucket(db, bucket_name="health_checks")

    test_data = b"\xC2\x50_health_check"  # 16 bytes, non-UTF-8 to prove binary safety

    # Upload
    file_id = await bucket.upload_from_stream("health_check.bin", io.BytesIO(test_data))

    # Download
    buf = io.BytesIO()
    await bucket.download_to_stream(file_id, buf)
    downloaded = buf.getvalue()

    # Compare
    assert downloaded == test_data, (
        f"GridFS round-trip mismatch: sent {test_data!r}, got {downloaded!r}"
    )

    # Clean up
    await bucket.delete(file_id)

    logger.info("MongoDB GridFS round-trip verified")
