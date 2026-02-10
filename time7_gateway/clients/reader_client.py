import json
import os
from datetime import datetime, timezone

import httpx

from time7_gateway.services.database import upsert_latest_tag


class ImpinjReaderClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url 
        self._client = httpx.AsyncClient(auth=(username, password), timeout=None)

    async def stream_events(self):
        url = f"{self.base_url}/data/stream" 
        async with self._client.stream("GET", url) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                if not line:
                    continue
                yield json.loads(line)

    async def aclose(self):
        await self._client.aclose()


async def run_reader_stream(app):
    reader_base_url = os.getenv("READER_BASE_URL", "").strip()
    reader_user = os.getenv("READER_USER", "root").strip()
    reader_password = os.getenv("READER_PASSWORD", "").strip()

    client = ImpinjReaderClient(reader_base_url, reader_user, reader_password)

    active_tags = app.state.active_tags
    cache = app.state.tag_info_cache
    ias_lookup = app.state.ias_lookup

    try:
        async for ev in client.stream_events():
            if ev.get("eventType") != "tagInventory":
                continue

            tie = ev.get("tagInventoryEvent", {})
            tag_id = tie.get("epcHex")
            if not tag_id:
                continue

            seen_at = datetime.now(timezone.utc)

            active_tags.sync_seen([tag_id], seen_at=seen_at)

            # if its new tag
            if cache.get(tag_id) is None:
                auth, info = ias_lookup(tag_id)
                cache.set(tag_id, auth, info)
                upsert_latest_tag(tag_id=tag_id, seen_at=seen_at, auth=auth, info=info)

    finally:
        await client.aclose()