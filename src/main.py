from fastapi import FastAPI

from routes import base
from routes import data
import asyncio
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from helpers.config import get_settings
from stores.llm import LLMProviderFactory
from stores.llm import LLMProviderEnum

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Getting the enviroments settings
    settings = get_settings()
    app.mongo_client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    
    app.mongo_db = app.mongo_client.get_database(settings.MONGO_DB_DATABASE)
    
    llm_provider_factory = LLMProviderFactory(config= settings.model_dump())
    
    #setting generation client
    app.generation_client = llm_provider_factory.intialize_provider(provider_name= settings.GENERATION_BACKEND)
    app.generation_client.set_generagtion_model(model_id= settings.GENERATION_MODEL_ID)
    
    #setting embedding client 
    app.embedding_client = llm_provider_factory.intialize_provider(provider_name= settings.EMBEDDING_BACKEND )
    app.embedding_client.set_embedding_model(model_id= settings.EMBEDDING_MODEL_ID,
                                             vector_size= settings.EMBEDDING_MODEL_SIZE)
    
    yield
    app.mongo_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)
