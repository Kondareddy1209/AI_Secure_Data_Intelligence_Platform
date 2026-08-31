import time
from fastapi import APIRouter
from app.core.config import settings

start_time = time.time()
router = APIRouter()


@router.get("/health")
async def health():
    uptime = time.time() - start_time
    return {
        "status": "ok",
        "version": settings.app_version,
        "uptime_seconds": round(uptime, 2),
        "environment": settings.environment,
    }

