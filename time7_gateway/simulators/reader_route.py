from fastapi import APIRouter, Request, HTTPException, Body
from datetime import datetime, timezone
from typing import Any

from time7_gateway.simulators.ias_services import mock_ias_lookup
from time7_gateway.services.database import upsert_latest_tag

router = APIRouter()


@router.post("/reader/events")
def reader_events(request: Request, payload: Any = Body(...)):
    active_tags = request.app.state.active_tags
    cache = request.app.state.tag_info_cache

    tags_seen = 0
    product_info_fetched = 0

    if isinstance(payload, dict) and "tagIds" in payload:
        now = datetime.now(timezone.utc)

        for tag_id in payload.get("tagIds") or []:
            tag_id = str(tag_id)
            active_tags.mark_seen(tag_id, seen_at=now)
            tags_seen += 1

            if cache.get(tag_id) is None:
                auth, info = mock_ias_lookup(tag_id)
                cache.set(tag_id, auth, info)
                product_info_fetched += 1

                upsert_latest_tag(
                    tag_id=tag_id,
                    seen_at=now,
                    auth=auth,
                    info=info,
                )

        return {
            "ok": True,
            "tags_seen": tags_seen,
            "product_info_fetched": product_info_fetched,
        }

    raise HTTPException(status_code=400, detail="Invalid payload. Expect {'tagIds': [...]}") 