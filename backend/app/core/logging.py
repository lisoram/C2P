"""
Structured JSON logging setup.
Uses python-json-logger v4+ (pythonjsonlogger.json.JsonFormatter).
Every log record includes: timestamp (IST), level, logger name, message,
and any extra fields passed by the caller (e.g. request_id, path, duration_ms).
"""

import logging
import sys

from pythonjsonlogger.json import JsonFormatter

from app.core.config import settings


class _ISTFormatter(JsonFormatter):
    """
    Thin subclass that renames the standard LogRecord field names
    to our preferred JSON keys before serialisation.
    """

    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super().add_fields(log_record, record, message_dict)
        # Rename built-in keys to our schema
        log_record["timestamp"] = log_record.pop("asctime", None) or record.asctime if hasattr(record, 'asctime') else None
        log_record["level"] = log_record.pop("levelname", record.levelname)
        log_record["logger"] = log_record.pop("name", record.name)


def configure_logging() -> None:
    """Call once at application startup to install the JSON log handler."""
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = _ISTFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger. Use this everywhere instead of print()."""
    return logging.getLogger(name)
