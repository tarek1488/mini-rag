from fastapi import FastAPI , APIRouter
import os
from helpers.config import get_settings
base_router =  APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/welcome")
async def welcome():
    app_settings = get_settings()
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
     
    return{"APP name" : app_name, "APP version" : app_version}
