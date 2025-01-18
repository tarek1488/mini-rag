from fastapi import FastAPI , APIRouter
import os
base_router =  APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@base_router.get("/welcome")
def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
     
    return{"APP name" : app_name, "APP version" : app_version}
