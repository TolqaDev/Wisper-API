from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.transcription_service import transcription_service
from app.utils.auth import get_current_user
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/transcribe")
async def create_transcription(
        talent_id: str = Form(...),
        acc_id: str = Form(...),
        mp3_file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
        request: Request = Request
):
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    try:
        if not talent_id or not acc_id:
            raise HTTPException(
                status_code=400,
                detail="talent_id ve acc_id zorunlu alanlardır"
            )

        if not mp3_file:
            raise HTTPException(
                status_code=400,
                detail="mp3_file zorunlu alandır"
            )

        success, message, job_uuid = transcription_service.create_transcription_job(
            db,
            talent_id,
            acc_id,
            mp3_file,
            client_ip=client_ip,
            api_processing_time_ms=(time.time() - start_time) * 1000
        )

        execution_time_ms = (time.time() - start_time) * 1000

        if success:
            logger.info(f"Yeni dönüştürme işi oluşturuldu - UUID: {job_uuid}, Talent: {talent_id}, Account: {acc_id}")
            return {
                "success": True,
                "message": message,
                "job_id": job_uuid,
                "status": "pending",
                "request_details": {
                    "client_ip": client_ip,
                    "execution_time_ms": round(execution_time_ms, 2),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        else:
            logger.warning(f"Dönüştürme işi oluşturulamadı - Talent: {talent_id}, Hata: {message}")
            raise HTTPException(status_code=400, detail=message)

    except HTTPException:
        raise
    except Exception as e:
        execution_time_ms = (time.time() - start_time) * 1000
        logger.error(f"Dönüştürme işi oluşturma hatası: {e}")
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


@router.get("/transcribe/{job_id}")
async def get_transcription_status(
        job_id: str,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
        request: Request = Request
):
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    try:
        job_info = transcription_service.get_transcription_status(db, job_id)

        execution_time_ms = (time.time() - start_time) * 1000

        if job_info:
            logger.info(f"İşlem durumu sorgulandı - UUID: {job_id}")
            return {
                "success": True,
                "job": job_info,
                "request_details": {
                    "client_ip": client_ip,
                    "execution_time_ms": round(execution_time_ms, 2),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        else:
            logger.warning(f"İşlem bulunamadı - UUID: {job_id}")
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "İşlem bulunamadı",
                    "request_details": {
                        "client_ip": client_ip,
                        "execution_time_ms": round(execution_time_ms, 2),
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    }
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        execution_time_ms = (time.time() - start_time) * 1000
        logger.error(f"İşlem durumu sorgulama hatası: {e}")
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


@router.get("/transcribe/{job_id}/cancel")
async def cancel_transcription(
        job_id: str,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
        request: Request = Request
):
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    try:
        success, message = transcription_service.cancel_transcription_job(db, job_id)

        execution_time_ms = (time.time() - start_time) * 1000

        if success:
            logger.info(f"İşlem iptal edildi - UUID: {job_id}")
            return {
                "success": True,
                "message": message,
                "request_details": {
                    "client_ip": client_ip,
                    "execution_time_ms": round(execution_time_ms, 2),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        else:
            logger.warning(f"İşlem iptal edilemedi - UUID: {job_id}, Sebep: {message}")
            raise HTTPException(
                status_code=400,
                detail={
                    "message": message,
                    "request_details": {
                        "client_ip": client_ip,
                        "execution_time_ms": round(execution_time_ms, 2),
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    }
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        execution_time_ms = (time.time() - start_time) * 1000
        logger.error(f"İşlem iptal etme hatası: {e}")
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
