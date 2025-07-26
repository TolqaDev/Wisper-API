from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)):
    token = credentials.credentials

    if token == settings.API_SECRET_TOKEN:
        logger.info("API token doğrulandı.")
        return "authenticated_user"
    else:
        logger.warning("Geçersiz API token denemesi.")
        raise HTTPException(
            status_code=401,
            detail="Geçersiz kimlik doğrulama tokenı",
            headers={"WWW-Authenticate": "Bearer"},
        )
