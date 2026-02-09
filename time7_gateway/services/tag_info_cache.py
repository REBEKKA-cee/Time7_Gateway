from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Tuple


@dataclass
class TagInfo:
    auth: bool
    info: Optional[str]
    fetched_at: datetime


class TagInfoCache:


    #caches IAS results. Avoid repeating checking with IAS

    def __init__(self, cache_ttl_hours: int = 24):
        self.cache_ttl = timedelta(hours=int(cache_ttl_hours))
        self._cache: Dict[str, TagInfo] = {}

    def get(self, tag_id: str) -> Optional[Tuple[bool, Optional[str]]]:
        cur = self._cache.get(tag_id)
        if cur is None:
            return None

        now = datetime.now(timezone.utc)
        if now - cur.fetched_at > self.cache_ttl:
            del self._cache[tag_id]
            return None

        return (cur.auth, cur.info)

    def set(self, tag_id: str, auth: bool, info: Optional[str]) -> None:
        self._cache[tag_id] = TagInfo(
            auth=auth,
            info=info,
            fetched_at=datetime.now(timezone.utc),
        )