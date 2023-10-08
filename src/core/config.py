import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from core.logger import LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    """Application settings and configuration."""

    DB_NAME: str = os.environ.get('POSTGRES_DB')
    DB_USER: str = os.environ.get('POSTGRES_USER')
    DB_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
    DB_HOST: str = os.environ.get('POSTGRES_HOST')
    DB_PORT: int = os.environ.get('POSTGRES_PORT')

    VIN_SERVICE_URL: str = 'http://18.202.200.86:9099/private/vin/decodes/{vin}/'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'allow'


settings = Settings()
