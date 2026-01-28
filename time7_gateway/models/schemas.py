from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .enums import AuthResult


class ScanEventRequest(BaseModel):
    """Scan event uploaded from the client system.
    This is the payload that /api/verify will receive.
    """

    epc: str = Field(..., description="EPC code (unique identifier of RFID tag)")
    token: Optional[str] = Field(
        default=None,
        description="Optional: client authentication/session token",
    )
    reader_id: Optional[str] = Field(
        default=None,
        description="Reader ID (Times-7 or third-party reader)",
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Timestamp of the scan event; if omitted, server time will be used",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "epc": "303400000000000000000001",
                "token": "customer-session-token",
                "reader_id": "reader-001",
                "timestamp": "2025-01-29T08:00:00Z",
            }
        }


class VerifyResponse(BaseModel):
    """Standardized response returned to the client system."""

    epc: str
    result: AuthResult
    message: str = "OK"
    reader_id: Optional[str] = None
    timestamp: datetime
    impinj_raw: Optional[dict] = None  # Raw Impinj response (optional for debugging)


class LogEntry(BaseModel):
    """Log entry structure for writing logs into JSON or database storage."""

    epc: str
    result: AuthResult
    reader_id: Optional[str] = None
    timestamp: datetime
    source: str = "gateway"  # e.g. gateway / test / mock
