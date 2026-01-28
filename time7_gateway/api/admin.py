from fastapi import APIRouter

router = APIRouter()

@router.get("/logs/health")
def logs_health():
    return {"service": "admin-logs", "status": "ok"}
