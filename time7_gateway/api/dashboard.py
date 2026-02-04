from fastapi import APIRouter, Request
from time7_gateway.models.schemas import ScanResult

router = APIRouter()


@router.get("/active-tags", response_model=list[ScanResult])
def active_tags(request: Request):
    active_tags = request.app.state.active_tags
    cache = request.app.state.tag_info_cache

    results: list[ScanResult] = []

    for t in active_tags.get_active():
        cached = cache.get(t.tag_id)
        if cached is None:
            continue

        auth, info = cached
        results.append(
            ScanResult(
                id=t.tag_id,
                date=t.last_seen,
                auth=auth,
                info=info,
            )
        )

    return results