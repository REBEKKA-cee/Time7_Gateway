from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class ReaderEventBatch(BaseModel):
    tagIds: List[str]


class ScanResult(BaseModel):
    id: str
    date: datetime
    auth: bool
    info: Optional[str] = None