from fastapi import APIRouter, Request

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/active-tags")
def active_tags_pre_ias(request: Request):
    """
    Returns what ActiveTags currently holds before sending to IAS
    """
    return request.app.state.active_tags.snapshot()

@router.get("/post-ias")
def post_ias_snapshot(request: Request):
    """
    TagInfoCache snapshot (POST-IAS) in the same fields dashboard/DB uses.
    """
    return request.app.state.tag_info_cache.snapshot()