from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

from fastapi import APIRouter, Body, HTTPException, Request

from time7_gateway.services.database import upsert_latest_tag

router = APIRouter()


def _parse_iso8601(s: str | None) -> datetime | None:
    if not s or not isinstance(s, str):
        return None

    # Handle trailing "Z" (UTC) to make it ISO8601-compatible for fromisoformat()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None

    # Ensure timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt


def _iter_events(payload: Any) -> Iterable[dict]:
    """
    Impinj webhook
    """
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
        return

    if isinstance(payload, dict):
        yield payload
        return


@router.post("/reader/webhook")
def reader_webhook(request: Request, payload: Any = Body(...)):
    """
    Receives Impinj "ReaderEvent" payloads.
    Extracts:
      - tag_id: tagInventoryEvent.epcHex (fallback tidHex)
      - seen_at: tagInventoryEvent.lastSeenTime (fallback event timestamp, then server now)
    """

    active_tags = request.app.state.active_tags
    cache = request.app.state.tag_info_cache

    ias_lookup = getattr(request.app.state, "ias_lookup", None)
    if not callable(ias_lookup):
        raise HTTPException(status_code=500, detail="IAS lookup not configured")

    tags_seen = 0
    product_info_fetched = 0
    ignored = 0

    for ev in _iter_events(payload):
        event_type = ev.get("eventType")

        if event_type != "tagInventory":
            ignored += 1
            continue

        tie = ev.get("tagInventoryEvent") or {}
        if not isinstance(tie, dict):
            ignored += 1
            continue

        tag_id = tie.get("epcHex") or tie.get("tidHex")
        if not tag_id:
            ignored += 1
            continue
        tag_id = str(tag_id)

        seen_at = (
            _parse_iso8601(tie.get("lastSeenTime"))
            or _parse_iso8601(ev.get("timestamp"))
            or datetime.now(timezone.utc)
        )

        active_tags.mark_seen(tag_id, seen_at=seen_at)
        tags_seen += 1

        # Only do IAS + DB work for new/uncached tags
        if cache.get(tag_id) is None:
            auth, info = ias_lookup(tag_id)
            cache.set(tag_id, auth, info)
            product_info_fetched += 1

            upsert_latest_tag(
                tag_id=tag_id,
                seen_at=seen_at,
                auth=auth,
                info=info,
            )

    # must acknowledge reader
    return {
        "ok": True,
        "tags_seen": tags_seen,
        "product_info_fetched": product_info_fetched,
        "ignored_events": ignored,
    }