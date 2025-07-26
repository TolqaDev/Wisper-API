import greenstalk
import json
import logging
from app.config.settings import settings
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class QueueService:

    def __init__(self):
        self.tube_name = "transcription_queue"

    def get_client(self) -> greenstalk.Client:
        try:
            client = greenstalk.Client(
                address=(settings.BEANSTALK_HOST, settings.BEANSTALK_PORT)
            )
            return client
        except Exception as e:
            logger.error(f"Greenstalk bağlantı hatası: {e}")
            raise

    def add_job(self, job_data: Dict[str, Any], priority: int = 1024) -> bool:
        client = None
        try:
            client = self.get_client()
            client.use(self.tube_name)

            job_json = json.dumps(job_data)
            job_id = client.put(job_json, priority=priority)

            logger.info(f"İş kuyruğa eklendi - Job ID: {job_id}, UUID: {job_data.get('uuid')}")
            return True

        except Exception as e:
            logger.error(f"Kuyruğa iş ekleme hatası: {e}")
            return False
        finally:
            if client:
                try:
                    client.close()
                except Exception as close_e:
                    logger.warning(f"Greenstalk istemcisini kapatırken hata: {close_e}")

    def get_queue_stats(self) -> Dict[str, int]:
        client = None
        try:
            client = self.get_client()
            stats = client.stats_tube(self.tube_name)

            return {
                "total_jobs": stats.get("total-jobs", 0),
                "ready_jobs": stats.get("current-jobs-ready", 0),
                "reserved_jobs": stats.get("current-jobs-reserved", 0),
                "buried_jobs": stats.get("current-jobs-buried", 0)
            }

        except Exception as e:
            logger.error(f"Kuyruk istatistikleri alınamadı: {e}")
            return {
                "total_jobs": 0,
                "ready_jobs": 0,
                "reserved_jobs": 0,
                "buried_jobs": 0
            }
        finally:
            if client:
                try:
                    client.close()
                except Exception as close_e:
                    logger.warning(f"Greenstalk istemcisini kapatırken hata: {close_e}")

    def cancel_job_by_uuid(self, target_uuid: str) -> bool:
        client = None
        try:
            client = self.get_client()
            client.watch(self.tube_name)

            while True:
                try:
                    job = client.reserve(timeout=1)
                    job_data = json.loads(job.body)

                    if job_data.get("uuid") == target_uuid:
                        client.delete(job)
                        logger.info(f"İş iptal edildi - UUID: {target_uuid}")
                        return True
                    else:
                        client.release(job)

                except greenstalk.TimedOutError:
                    break

            return False

        except Exception as e:
            logger.error(f"İş iptal etme hatası: {e}")
            return False
        finally:
            if client:
                try:
                    client.close()
                except Exception as close_e:
                    logger.warning(f"Greenstalk istemcisini kapatırken hata: {close_e}")


queue_service = QueueService()
