from fastapi import APIRouter

from time7_gateway.models.schemas import ScanEventRequest, VerifyResponse
from time7_gateway.services.auth_service import AuthService
from time7_gateway.clients.impinj_mock import ImpinjMockClient

router = APIRouter(tags=["verify"])

# Single shared instance for the whole app
auth_service = AuthService(ImpinjMockClient())


@router.get("/verify/health")
async def verify_health():
    return {"service": "verify", "status": "ok"}


@router.post("/verify", response_model=VerifyResponse)
async def verify_tag(payload: ScanEventRequest):
    """Verify one EPC using the mock Impinj flow."""
    return await auth_service.verify(payload)
