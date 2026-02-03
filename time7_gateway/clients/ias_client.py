# time7_gateway/clients/ias_client.py
from typing import Any, Dict, Optional

import httpx
from time7_gateway.models.enums import AuthResult


class IASClient:
    """HTTP client that talks to Mock IAS (port 8200)."""

    def __init__(self, base_url: str = "http://127.0.0.1:8200") -> None:
        self.base_url = base_url

    async def verify_epc(
        self,
        epc: str,
        token: Optional[str] = None,
        reader_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> tuple[AuthResult, Dict[str, Any]]:
        """
        调用 Mock IAS 的 /verify 接口，并把结果映射成 AuthResult。
        """
        url = f"{self.base_url}/verify"

        payload: Dict[str, Any] = {
            "epc": epc,
            "token": token,
            "reader_id": reader_id,
            "timestamp": timestamp,
        }

        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()

        data = resp.json()
        result = data.get("result", "unknown")

        # 映射到我们统一的 AuthResult 枚举
        if result == "authentic":
            mapped = AuthResult.AUTHENTIC
        elif result == "tampered":
            mapped = AuthResult.TAMPERED
        elif result == "mismatch":
            mapped = AuthResult.MISMATCH
        else:
            mapped = AuthResult.UNKNOWN

        return mapped, data
