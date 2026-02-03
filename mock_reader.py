# mock_reader.py - Official-like Impinj Reader Event JSON Mock

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI()

# ---- 官方格式 TagEvent ----
class Tag(BaseModel):
    epc: str
    antenna: int
    rssi: float
    timestamp: str  # ISO8601

class ReaderEvent(BaseModel):
    readerId: str                # 官方命名
    eventId: Optional[str] = None
    type: Optional[str] = "TAG_REPORT"
    tags: List[Tag]


@app.get("/health")
def health():
    return {"service": "mock-reader", "status": "ok"}


@app.post("/data/stream")
async def stream(event: ReaderEvent):
    """
    接收 ReaderEvent（包含多个 Tag）
    再把每个 Tag --> Gateway (/api/verify/verify)
    """

    gateway_url = "http://127.0.0.1:8000/api/verify"

    results = []

    async with httpx.AsyncClient() as client:
        for tag in event.tags:
            payload = {
                "epc": tag.epc,
                "reader_id": event.readerId,   # Gateway 用的是 snake_case
                "timestamp": tag.timestamp
            }

            print("➡️ Sending to Gateway:", payload)

            resp = await client.post(gateway_url, json=payload)
            results.append(resp.json())

    return {
        "message": "OK",
        "readerId": event.readerId,
        "sent_tags": len(results),
        "results": results,
    }
