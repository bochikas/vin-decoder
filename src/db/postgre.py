import logging

from databases import Database

from core.config import settings

logger = logging.getLogger()

db_url = (f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
          f'{settings.DB_PORT}/{settings.DB_NAME}')

logging.info(f'Defining configuration for db at [postgresql://'
             f'{settings.DB_USER}:****@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}]')

database: Database = Database(db_url, min_size=5, max_size=20)


async def get_database() -> Database:
    return database
