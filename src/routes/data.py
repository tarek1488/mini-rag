from fastapi import FastAPI , APIRouter, Depends, UploadFile
import os
from helpers.config import get_settings, Settings
from controllers import DataController

data_router =  APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    #validate the uploaded file
    is_valid, result_message = DataController().validate_file_uploaded(file = file)
    return is_valid
    