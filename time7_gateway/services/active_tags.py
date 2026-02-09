from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class ActiveTag:
    tag_id: str
    last_seen: datetime


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class ActiveTags:

    # tags in detection zone currently

    def __init__(self, active_ttl_seconds: int = 5):
        self.active_ttl_seconds = int(active_ttl_seconds)
        self._tags: Dict[str, ActiveTag] = {}

    def mark_seen(self, tag_id: str, seen_at: Optional[datetime] = None) -> ActiveTag:
        now = _utc(seen_at) if seen_at else datetime.now(timezone.utc)

        cur = self._tags.get(tag_id)
        if cur is None:
            cur = ActiveTag(tag_id=tag_id, last_seen=now)
            self._tags[tag_id] = cur
        else:
            cur.last_seen = now

        return cur

    def removeExpired(self) -> int:
        now = datetime.now(timezone.utc)
        ttl = self.active_ttl_seconds

        expired = [
            tid
            for tid, t in self._tags.items()
            if (now - t.last_seen).total_seconds() > ttl
        ]
        for tid in expired:
            del self._tags[tid]

        return len(expired)

    def get_active(self) -> List[ActiveTag]:
        self.removeExpired()
        return sorted(self._tags.values(), key=lambda x: x.last_seen, reverse=True)

    def get_active_ids(self) -> List[str]:
        self.removeExpired()
        return list(self._tags.keys())