import logging
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import json

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]

        start_time = time.time()

        await self._log_request(request, request_id)

        response = await call_next(request)

        process_time = time.time() - start_time

        self._log_response(response, request_id, process_time)

        response.headers["X-Request-ID"] = request_id

        return response

    async def _log_request(self, request: Request, request_id: str):
        try:
            client_ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "unknown")

            log_data = {
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": client_ip,
                "user_agent": user_agent,
                "headers": dict(request.headers),
                "query_params": dict(request.query_params)
            }

            if request.method in ["POST", "PUT", "PATCH"]:
                content_type = request.headers.get("content-type", "")

                if "multipart/form-data" in content_type:
                    log_data["body"] = "multipart/form-data (dosya yükleme)"
                elif "application/json" in content_type:
                    try:
                        body = await request.body()
                        if body:
                            log_data["body"] = json.loads(body.decode())
                    except:
                        log_data["body"] = "JSON parse hatası"
                else:
                    log_data["body"] = "binary/other content"

            logger.info(f"API İsteği - {json.dumps(log_data, ensure_ascii=False)}")

        except Exception as e:
            logger.error(f"İstek loglama hatası: {e}")

    def _log_response(self, response: Response, request_id: str, process_time: float):
        try:
            log_data = {
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time_ms": round(process_time * 1000, 2),
                "response_headers": dict(response.headers)
            }

            if response.status_code >= 500:
                logger.error(f"API Yanıtı - {json.dumps(log_data, ensure_ascii=False)}")
            elif response.status_code >= 400:
                logger.warning(f"API Yanıtı - {json.dumps(log_data, ensure_ascii=False)}")
            else:
                logger.info(f"API Yanıtı - {json.dumps(log_data, ensure_ascii=False)}")

        except Exception as e:
            logger.error(f"Yanıt loglama hatası: {e}")
