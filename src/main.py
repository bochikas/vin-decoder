import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import vehicles
from core.logger import LOGGING
from db.postgre import database

app = FastAPI(
    title='VIN decoder',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='The VIN Decoder API that provides information about vehicles based on their VIN numbers'
)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(vehicles.router, prefix='/api/v1/vehicles', tags=['vehicles'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
