import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/whisper_db")
    BEANSTALK_HOST: str = os.getenv("BEANSTALK_HOST", "localhost")
    BEANSTALK_PORT: int = int(os.getenv("BEANSTALK_PORT", "11300"))
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "25000000"))
    ALLOWED_AUDIO_FORMATS: list = ["mp3", "wav", "m4a", "flac"]
    API_SECRET_TOKEN: str = os.getenv("API_SECRET_TOKEN", "your-super-secret-token")

    _recordings_dir_env = os.getenv("RECORDINGS_DIR", "recordings")
    if not os.path.isabs(_recordings_dir_env):
        RECORDINGS_DIR: str = os.path.join(BASE_DIR, _recordings_dir_env)
    else:
        RECORDINGS_DIR: str = _recordings_dir_env

    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")


settings = Settings()
