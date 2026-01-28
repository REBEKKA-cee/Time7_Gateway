from typing import Any, Dict, Optional, Tuple

from time7_gateway.models.enums import AuthResult


class ImpinjMockClient:
    """Mock Impinj client for Phase 1.

    Rule:
      - EPC starting with '3034' -> AUTHENTIC
      - otherwise               -> MISMATCH
    """

    async def verify_epc(
        self,
        epc: str,
        token: Optional[str] = None,
        reader_id: Optional[str] = None,
    ) -> Tuple[AuthResult, Dict[str, Any]]:
        """Return a fake verification result for one EPC."""
        if epc.startswith("3034"):
            result = AuthResult.AUTHENTIC
        else:
            result = AuthResult.MISMATCH

        raw: Dict[str, Any] = {
            "mock": True,
            "rule": "epc startswith '3034' => authentic, else mismatch",
        }
        return result, raw
