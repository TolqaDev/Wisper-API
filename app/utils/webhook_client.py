import httpx
import logging
import asyncio
from typing import Dict, Any, Optional
from app.config.settings import settings
from datetime import datetime

logger = logging.getLogger(__name__)


class WebhookClient:

    def __init__(self):
        self.webhook_url = settings.WEBHOOK_URL
        self.max_retries = 3
        self.timeout = 30

    async def send_completion_webhook(
            self,
            uuid: str,
            talent_id: str,
            acc_id: str,
            text: str,
            client_ip: Optional[str] = None,
            api_processing_time_ms: Optional[float] = None,
            worker_execution_time_ms: Optional[float] = None
    ) -> bool:
        if not self.webhook_url:
            logger.warning("Webhook URL tanımlanmamış")
            return False

        payload = {
            "uuid": uuid,
            "talent_id": talent_id,
            "acc_id": acc_id,
            "text": text,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_details": {
                "client_ip": client_ip,
                "api_processing_time_ms": round(api_processing_time_ms,
                                                2) if api_processing_time_ms is not None else None,
                "worker_execution_time_ms": round(worker_execution_time_ms,
                                                  2) if worker_execution_time_ms is not None else None,
                "webhook_sent_timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        self.webhook_url,
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )

                    if response.status_code == 200:
                        logger.info(f"Webhook başarıyla gönderildi - UUID: {uuid}")
                        return True
                    else:
                        logger.warning(
                            f"Webhook hatası - UUID: {uuid}, "
                            f"Status: {response.status_code}, "
                            f"Deneme: {attempt + 1}"
                        )

            except Exception as e:
                logger.error(
                    f"Webhook gönderim hatası - UUID: {uuid}, "
                    f"Deneme: {attempt + 1}, Hata: {e}"
                )

            if attempt < self.max_retries - 1:
                await asyncio.sleep(2 ** attempt)

        logger.error(f"Webhook gönderilemedi - UUID: {uuid}, Tüm denemeler başarısız")
        return False


webhook_client = WebhookClient()
