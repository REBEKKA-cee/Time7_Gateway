from datetime import datetime
from time7_gateway.clients.supabase_client import get_supabase


def upsert_latest_tag(tag_id: str, seen_at: datetime, auth: bool, info: str | None):
    sb = get_supabase()
    payload = {
        "id": tag_id,
        "date": seen_at.isoformat(),
        "auth": auth,
        "info": info,
    }
    sb.table("data").upsert(payload).execute()