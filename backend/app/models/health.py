"""
Pydantic models for the health endpoint.
"""

from typing import Literal

from pydantic import BaseModel


ServiceState = Literal["ok", "error"]


class ServiceStatuses(BaseModel):
    postgres: ServiceState
    mongodb: ServiceState
    qdrant: ServiceState
    gemini: ServiceState


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    services: ServiceStatuses


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict = {}


class ErrorEnvelope(BaseModel):
    error: ErrorDetail
