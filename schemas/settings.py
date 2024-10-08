from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    local_user: str
    local_db: str
    local_db_password: str
    local_hostname: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


@lru_cache
def setting():
    return Settings()
