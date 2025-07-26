import greenstalk
import json
import whisper
import os
import logging
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.transcription import ConvertedSound
from app.services.transcription_service import TranscriptionService
from app.utils.webhook_client import WebhookClient
from app.config.settings import settings
from datetime import datetime
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('worker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TranscriptionWorker:

    def __init__(self):
        self.tube_name = "transcription_queue"
        self.whisper_model = None
        self.webhook_client = WebhookClient()

        self.engine = create_engine(settings.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def load_whisper_model(self):
        try:
            logger.info(f"Whisper modeli yükleniyor: {settings.WHISPER_MODEL}...")
            self.whisper_model = whisper.load_model(settings.WHISPER_MODEL)
            logger.info("Whisper modeli başarıyla yüklendi")
        except Exception as e:
            logger.error(f"Whisper modeli yüklenemedi: {e}")
            raise

    def get_queue_client(self) -> greenstalk.Client:
        return greenstalk.Client(
            address=(settings.BEANSTALK_HOST, settings.BEANSTALK_PORT)
        )

    async def process_job(self, job_data: dict):
        start_time = time.time()

        job_uuid = job_data.get("uuid")
        talent_id = job_data.get("talent_id")
        acc_id = job_data.get("acc_id")
        file_name = job_data.get("file_name")

        client_ip = job_data.get("client_ip", "unknown")
        api_processing_time_ms = job_data.get("api_processing_time_ms", 0.0)

        file_path = os.path.join(settings.RECORDINGS_DIR, file_name)

        db = self.SessionLocal()

        try:
            logger.info(f"İş işleniyor - UUID: {job_uuid}")

            record = db.query(ConvertedSound).filter(
                ConvertedSound.uuid == job_uuid
            ).first()

            if not record:
                logger.error(f"Veritabanında kayıt bulunamadı - UUID: {job_uuid}")
                return

            record.status = "processing"
            db.commit()

            logger.info(f"Worker dosya yolunu kontrol ediyor: {file_path}")
            if not os.path.exists(file_path):
                raise Exception(f"Ses dosyası bulunamadı: {file_path}")
            logger.info(f"Worker dosyayı buldu: {file_path}")

            logger.info(f"Ses dönüştürme başlatılıyor - UUID: {job_uuid}")
            result = self.whisper_model.transcribe(file_path)
            transcribed_text = result["text"].strip()

            if not transcribed_text:
                raise Exception("Dönüştürme sonucu boş metin")

            encoded_text = TranscriptionService.encode_text_md5(transcribed_text)

            record.text = transcribed_text
            record.encoded_text = encoded_text
            record.status = "success"
            db.commit()

            logger.info(f"Dönüştürme başarılı - UUID: {job_uuid}")

            worker_execution_time_ms = (time.time() - start_time) * 1000

            webhook_success = await self.webhook_client.send_completion_webhook(
                job_uuid,
                talent_id,
                acc_id,
                transcribed_text,
                client_ip=client_ip,
                api_processing_time_ms=api_processing_time_ms,
                worker_execution_time_ms=worker_execution_time_ms
            )

            if webhook_success:
                logger.info(f"Webhook başarıyla gönderildi - UUID: {job_uuid}")
            else:
                logger.warning(f"Webhook gönderilemedi - UUID: {job_uuid}")

            try:
                os.remove(file_path)
                logger.info(f"Geçici dosya silindi: {file_path}")
            except Exception as e:
                logger.warning(f"Geçici dosya silinemedi ({file_path}): {e}")

        except Exception as e:
            logger.error(f"İş işleme hatası - UUID: {job_uuid}, Hata: {e}")

            try:
                record.status = "error"
                record.error_message = str(e)
                db.commit()
            except Exception as db_e:
                logger.error(f"Hata durumu veritabanına kaydedilemedi - UUID: {job_uuid}, Hata: {db_e}")

            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Hata durumunda geçici dosya silindi: {file_path}")
            except Exception as file_e:
                logger.warning(f"Hata durumunda geçici dosya silinemedi ({file_path}): {file_e}")

        finally:
            db.close()

    async def run(self):
        logger.info("Transcription Worker başlatılıyor...")

        self.load_whisper_model()

        client = self.get_queue_client()
        client.watch(self.tube_name)

        logger.info(f"Kuyruk dinleniyor: {self.tube_name}")

        while True:
            try:
                job = client.reserve(timeout=30)

                try:
                    job_data = json.loads(job.body)
                    logger.info(f"Yeni iş alındı - UUID: {job_data.get('uuid')}")

                    await self.process_job(job_data)

                    client.delete(job)

                except Exception as e:
                    logger.error(f"İş işleme hatası: {e}")
                    client.release(job, delay=60)

            except greenstalk.TimedOutError:
                logger.debug("Kuyruk timeout - beklemeye devam")
                continue

            except Exception as e:
                logger.error(f"Worker hatası: {e}")
                await asyncio.sleep(5)


if __name__ == "__main__":
    worker = TranscriptionWorker()
    asyncio.run(worker.run())
