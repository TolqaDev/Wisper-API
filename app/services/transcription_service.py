import hashlib
import os
import tempfile
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.transcription import ConvertedSound
from app.services.queue_service import queue_service
import logging
import uuid as uuid_lib
from app.config.settings import settings

logger = logging.getLogger(__name__)


class TranscriptionService:

    def create_transcription_job(
            self,
            db: Session,
            talent_id: str,
            acc_id: str,
            audio_file,
            client_ip: str,
            api_processing_time_ms: float
    ) -> Tuple[bool, str, Optional[str]]:
        try:
            is_valid, error_msg = self._validate_audio_file(audio_file)
            if not is_valid:
                return False, error_msg, None

            job_uuid = str(uuid_lib.uuid4())

            host_temp_file_path = self._save_temp_file(audio_file, job_uuid)
            if not host_temp_file_path:
                return False, "Dosya kaydedilemedi", None

            file_name_for_queue = os.path.basename(host_temp_file_path)

            logger.info(f"Kuyruğa gönderilen dosya adı: {file_name_for_queue}")

            db_record = ConvertedSound(
                uuid=job_uuid,
                talent_id=talent_id,
                acc_id=acc_id,
                status="pending"
            )

            db.add(db_record)
            db.commit()

            job_data = {
                "uuid": job_uuid,
                "talent_id": talent_id,
                "acc_id": acc_id,
                "file_name": file_name_for_queue,
                "client_ip": client_ip,
                "api_processing_time_ms": api_processing_time_ms
            }

            if queue_service.add_job(job_data):
                logger.info(f"Yeni dönüştürme işi oluşturuldu - UUID: {job_uuid}")
                return True, "İşlem başarıyla oluşturuldu", job_uuid
            else:
                db.delete(db_record)
                db.commit()
                if os.path.exists(host_temp_file_path):
                    os.remove(host_temp_file_path)
                    logger.warning(f"Kuyruk hatası nedeniyle geçici dosya silindi: {host_temp_file_path}")
                return False, "Kuyruk sistemi hatası", None

        except Exception as e:
            logger.error(f"Dönüştürme işi oluşturma hatası: {e}")
            db.rollback()
            return False, "Sistem hatası", None

    def get_transcription_status(self, db: Session, job_uuid: str) -> Optional[dict]:
        try:
            record = db.query(ConvertedSound).filter(
                ConvertedSound.uuid == job_uuid
            ).first()

            if record:
                return record.to_dict()
            return None

        except Exception as e:
            logger.error(f"İşlem durumu sorgulama hatası: {e}")
            return None

    def cancel_transcription_job(self, db: Session, job_uuid: str) -> Tuple[bool, str]:
        try:
            record = db.query(ConvertedSound).filter(
                ConvertedSound.uuid == job_uuid
            ).first()

            if not record:
                return False, "İşlem bulunamadı"

            if record.status != "pending":
                return False, f"İşlem iptal edilemez. Mevcut durum: {record.status}"

            if queue_service.cancel_job_by_uuid(job_uuid):
                record.status = "cancelled"
                db.commit()
                logger.info(f"İşlem iptal edildi - UUID: {job_uuid}")

                recordings_dir = settings.RECORDINGS_DIR

                for filename in os.listdir(recordings_dir):
                    if filename.startswith(job_uuid):
                        file_to_delete = os.path.abspath(os.path.join(recordings_dir, filename))
                        try:
                            os.remove(file_to_delete)
                            logger.info(f"İptal edilen işin geçici dosyası silindi: {file_to_delete}")
                        except Exception as e:
                            logger.warning(f"İptal edilen işin geçici dosyası silinemedi ({file_to_delete}): {e}")
                        break

                return True, "İşlem başarıyla iptal edildi"
            else:
                return False, "İşlem kuyruktan iptal edilemedi"

        except Exception as e:
            logger.error(f"İşlem iptal etme hatası: {e}")
            db.rollback()
            return False, "Sistem hatası"

    def _validate_audio_file(self, audio_file) -> Tuple[bool, str]:
        try:
            if audio_file.size > settings.MAX_FILE_SIZE:
                return False, f"Dosya boyutu {settings.MAX_FILE_SIZE / (1024 * 1024)}MB'dan büyük olamaz"

            file_extension = audio_file.filename.split('.')[-1].lower()

            if file_extension not in settings.ALLOWED_AUDIO_FORMATS:
                return False, f"Desteklenmeyen dosya formatı. İzin verilen formatlar: {', '.join(settings.ALLOWED_AUDIO_FORMATS)}"

            content_type = audio_file.content_type
            allowed_mime_types = [
                "audio/mpeg", "audio/mp3", "audio/wav",
                "audio/x-wav", "audio/mp4", "audio/flac"
            ]

            if content_type not in allowed_mime_types:
                return False, "Geçersiz dosya türü"

            return True, ""

        except Exception as e:
            logger.error(f"Dosya doğrulama hatası: {e}")
            return False, "Dosya doğrulama hatası"

    def _save_temp_file(self, audio_file, job_uuid: str) -> Optional[str]:
        try:
            recordings_dir = settings.RECORDINGS_DIR
            os.makedirs(recordings_dir, exist_ok=True)

            file_extension = audio_file.filename.split('.')[-1].lower()

            temp_file_path = os.path.abspath(os.path.join(recordings_dir, f"{job_uuid}.{file_extension}"))

            with open(temp_file_path, "wb") as temp_file:
                content = audio_file.file.read()
                temp_file.write(content)

            logger.info(f"Ses dosyası kaydedildi (Host): {temp_file_path}")
            return temp_file_path

        except Exception as e:
            logger.error(f"Ses dosyası kaydetme hatası (Host): {e}")
            return None

    @staticmethod
    def encode_text_md5(text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()


transcription_service = TranscriptionService()
