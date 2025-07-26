from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.queue_service import queue_service
from app.models.transcription import ConvertedSound
from app.utils.auth import get_current_user
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def get_health_status(
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
        request: Request = Request
):
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    try:
        queue_stats = queue_service.get_queue_stats()

        db_stats = {
            "pending": db.query(ConvertedSound).filter(ConvertedSound.status == "pending").count(),
            "processing": db.query(ConvertedSound).filter(ConvertedSound.status == "processing").count(),
            "success": db.query(ConvertedSound).filter(ConvertedSound.status == "success").count(),
            "error": db.query(ConvertedSound).filter(ConvertedSound.status == "error").count(),
            "cancelled": db.query(ConvertedSound).filter(ConvertedSound.status == "cancelled").count()
        }

        system_status = "healthy"
        if queue_stats["total_jobs"] == 0 and db_stats["pending"] > 0:
            system_status = "warning"

        execution_time_ms = (time.time() - start_time) * 1000

        response = {
            "status": system_status,
            "queue": {
                "total_jobs": queue_stats["total_jobs"],
                "ready_jobs": queue_stats["ready_jobs"],
                "processing_jobs": queue_stats["reserved_jobs"],
                "buried_jobs": queue_stats["buried_jobs"]
            },
            "database": db_stats,
            "summary": f"Toplam {queue_stats['total_jobs']} iş, {queue_stats['ready_jobs']} bekleyen, {queue_stats['reserved_jobs']} işlemde",
            "request_details": {
                "client_ip": client_ip,
                "execution_time_ms": round(execution_time_ms, 2),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }

        logger.info("Sistem sağlık durumu sorgulandı")
        return response

    except Exception as e:
        execution_time_ms = (time.time() - start_time) * 1000
        logger.error(f"Sağlık durumu sorgulama hatası: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Sistem hatası",
                "error": str(e),
                "request_details": {
                    "client_ip": client_ip,
                    "execution_time_ms": round(execution_time_ms, 2),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )
