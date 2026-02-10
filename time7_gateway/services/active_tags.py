from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Iterable, List, Optional, Set


@dataclass
class ActiveTag:
    tag_id: str
    first_seen: datetime     
    last_seen: datetime      


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class ActiveTags:
    def __init__(self, remove_grace_seconds: float = 2.0) -> None:
        self._tags: Dict[str, ActiveTag] = {}
        self._grace = timedelta(seconds=float(remove_grace_seconds))

    def sync_seen(self, tag_ids: Iterable[str], seen_at: Optional[datetime] = None) -> Set[str]:

        now = _utc(seen_at) if seen_at else datetime.now(timezone.utc)
        seen_now = {str(t) for t in (tag_ids or [])}

        new_ids: Set[str] = set()

        # Add new tags, refresh last_seen for existing tags that appear again
        for tid in seen_now:
            cur = self._tags.get(tid)
            if cur is None:
                self._tags[tid] = ActiveTag(tag_id=tid, first_seen=now, last_seen=now)
                new_ids.add(tid)
            else:
                # Only refresh last_seen 
                cur.last_seen = now

        # Remove tags that haven't been seen in the last 2 seconds
        cutoff = now - self._grace
        for tid in list(self._tags.keys()):
            if self._tags[tid].last_seen < cutoff:
                del self._tags[tid]

        return new_ids

    def get_active(self) -> List[ActiveTag]:
 
        return sorted(self._tags.values(), key=lambda x: x.first_seen, reverse=True)

    def get_active_ids(self) -> List[str]:
        return list(self._tags.keys())
    
    #for debugging
    def snapshot(self) -> dict:
        items = [
            {
                "id": t.tag_id,
                "first_seen": t.first_seen,
                "last_seen": t.last_seen,
            }
            for t in self.get_active()
        ]

        return {"count": len(items), "items": items}    