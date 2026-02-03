from fastapi import APIRouter

from time7_gateway.models.schemas import ScanEventRequest, VerifyResponse
from time7_gateway.services.auth_service import AuthService
from time7_gateway.clients.ias_client import IASClient


router = APIRouter(tags=["verify"])

# 使用 IASClient（最终会调用 http://127.0.0.1:8200/verify）
auth_service = AuthService(IASClient())


@router.get("/verify/health")
async def verify_health():
    return {"service": "verify", "status": "ok"}


@router.post("/verify", response_model=VerifyResponse)
async def verify_tag(payload: ScanEventRequest):
    """入口：前端 / Mock Reader 把 EPC 扫描事件发到这里。"""
    return await auth_service.verify(payload)
