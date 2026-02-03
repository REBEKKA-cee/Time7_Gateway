from datetime import datetime

from time7_gateway.models.schemas import ScanEventRequest, VerifyResponse
from time7_gateway.clients.ias_client import IASClient


class AuthService:
    """Core authentication flow using IAS (via Mock IAS service)."""

    def __init__(self, ias_client: IASClient) -> None:
        self._ias = ias_client

    async def verify(self, event: ScanEventRequest) -> VerifyResponse:
        # 如果前端没有传时间，就用服务器当前时间
        ts = event.timestamp or datetime.utcnow()

        # 调用 IASClient 的 verify_epc（接口与之前 ImpinjMockClient 保持一致）
        result, raw = await self._ias.verify_epc(
            epc=event.epc,
            token=event.token,
            reader_id=event.reader_id,
            timestamp=ts.isoformat(),
        )

        # 组装成统一的响应模型
        return VerifyResponse(
            epc=event.epc,
            result=result,
            message="OK",
            reader_id=event.reader_id,
            timestamp=ts,
            impinj_raw=raw,
        )
