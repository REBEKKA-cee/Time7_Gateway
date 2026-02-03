# mock_ias.py
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Mock IAS Service")

class IASRequest(BaseModel):
    epc: str
    reader_id: str
    timestamp: datetime

class IASResponse(BaseModel):
    result: str
    details: dict

@app.get("/health")
def health():
    return {"service": "mock-ias", "status": "ok"}

@app.post("/verify", response_model=IASResponse)
def verify(req: IASRequest):
    # 模拟 IAS 验证规则：EPC 以 "3034" 开头 = authentic
    if req.epc.startswith("3034"):
        result = "authentic"
    else:
        result = "mismatch"

    return IASResponse(
        result=result,
        details={
            "epc": req.epc,
            "reader_id": req.reader_id,
            "verified_at": datetime.utcnow(),
        }
    )
