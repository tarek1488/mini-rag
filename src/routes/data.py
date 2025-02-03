from fastapi import FastAPI , APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest

logger = logging.getLogger('uvicorn.error')

data_router =  APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    data_controller = DataController()
    #validate the uploaded file
    is_valid, result_message = data_controller.validate_file_uploaded(file = file)
    
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"repsonse signal" : result_message})
    # Now file is valid
    
    #getting project directory
    # project_directory = ProjectController().get_project_path(project_id=project_id)
    
    file_path, unique_fileID = data_controller.generate_unique_file_path(original_file_name=file.filename, project_id= project_id)    
    #loading file by chunks
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f'File upload error: {e}')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"response signal" : ResponseSignal.FILE_UPLOADED_FAIL.value})
    
    return JSONResponse(content={"repsonse signal" : ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                                 "File ID": unique_fileID})
    
    
    
@data_router.post("/process/{project_id}")
async def process_file(project_id: str, process_request: ProcessRequest):
    process_controller = ProcessController(project_id=project_id)
    file_id = process_request.FILE_ID
    overlap = process_request.OVERLAP
    chunk_size = process_request.CHUNK_SIZE
    
    file_content = process_controller.get_file_content(file_id= file_id)
    
    #spltting file content to chunks
    
    file_chunks = process_controller.split_file_content(file_content=file_content,
                                                        chunk_size=chunk_size,
                                                        overlap=overlap)
    if len(file_chunks) == 0 or file_chunks == None:
        return JSONResponse(
            content={"response signal": ResponseSignal.FILE_PROCESSING_FALIED.value},
            status_code= status.HTTP_400_BAD_REQUEST
        )
    
    return JSONResponse(
    content={
        "response signal": ResponseSignal.FILE_PROCESSING_SUCCEED.value,
        "file chunks": [chunk.model_dump() if hasattr(chunk, "model_dump") else vars(chunk) for chunk in file_chunks]
    }
)

    #return file_chunks