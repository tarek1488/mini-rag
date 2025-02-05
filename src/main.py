from fastapi import FastAPI

from routes import base
from routes import data
import asyncio
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from helpers.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Getting the enviroments settings
    settings = get_settings()
    app.mongo_client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    
    app.mongo_db = app.mongo_client.get_database(settings.MONGO_DB_DATABASE)
    yield
    app.mongo_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)
