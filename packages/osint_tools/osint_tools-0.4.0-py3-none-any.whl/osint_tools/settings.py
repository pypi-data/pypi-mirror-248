from functools import lru_cache
from pydantic import BaseSettings
from os import environ
from typing import Optional

class _BaseSettings(BaseSettings):
    WHICH_LOGGER: str = environ.get('WHICH_LOGGER')
    LOG_FILE_PATH: Optional[str] = None
    MONGO_URI: str = environ.get('MONGO_URI')
    MONGO_DB_NAME: str = environ.get('MONGO_DB_NAME')

@lru_cache()
def get_settings() -> BaseSettings:
    return _BaseSettings()
