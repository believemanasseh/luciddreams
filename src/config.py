import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str
    DB_PASS: str
    DB_USER: str

    model_config = SettingsConfigDict(env_file=env_file_path)


settings = Settings()
