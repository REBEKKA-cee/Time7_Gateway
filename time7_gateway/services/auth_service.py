from datetime import datetime

from time7_gateway.models.schemas import ScanEventRequest, VerifyResponse
from time7_gateway.clients.impinj_mock import ImpinjMockClient


class AuthService:
    """Core authentication flow using an Impinj-like client."""

    def __init__(self, impinj_client: ImpinjMockClient) -> None:
        self._impinj = impinj_client

    async def verify(self, event: ScanEventRequest) -> VerifyResponse:
        # Use event.timestamp if provided; otherwise use server time
        ts = event.timestamp or datetime.utcnow()

        # Call mock Impinj client
        result, raw = await self._impinj.verify_epc(
            epc=event.epc,
            token=event.token,
            reader_id=event.reader_id,
        )

        # Build standard response to customer system
        return VerifyResponse(
            epc=event.epc,
            result=result,
            reader_id=event.reader_id,
            timestamp=ts,
            impinj_raw=raw,
        )
