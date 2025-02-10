from fastapi import FastAPI , APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal
from models import AssetTypeEnum
import logging
from .schemes.data import ProcessRequest
from models import ProjectDataModel, ChunkDataModel, AssetDataModel
from models.db_schemes.data_chunk import DataChunk
from models.db_schemes.asset import Asset

logger = logging.getLogger('uvicorn.error')

data_router =  APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_file(request: Request,project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    db = request.app.mongo_db
    project_data_model = await ProjectDataModel.initialize_project_model(db_client=db)
    project = await project_data_model.get_or_create_project(project_id=project_id)
    
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
    
    asset_data_model = await AssetDataModel.initialize_asset_model(db_client=db)
    
    asset_record = await asset_data_model.create_asset(asset= Asset(
        asset_name=  unique_fileID,
        asset_project_id= project.id,
        asset_type= AssetTypeEnum.FILE.value,
        asset_size= os.path.getsize(file_path)
        
    ))
    
    return JSONResponse(content={"repsonse signal" : ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                                 "File ID": str(asset_record.id)})
    
    
    
@data_router.post("/process/{project_id}")
async def process_file(request: Request, project_id: str, process_request: ProcessRequest):
    db = request.app.mongo_db
    chunk_data_model = await ChunkDataModel.initialize_chunk_model(db_client=db)
    
    project_data_model = await ProjectDataModel.initialize_project_model(db_client=db)
    project = await project_data_model.get_or_create_project(project_id=project_id)
    
    process_controller = ProcessController(project_id=project_id)
    #file_id = process_request.FILE_ID
    overlap = process_request.OVERLAP
    chunk_size = process_request.CHUNK_SIZE
    do_reset = process_request.DO_RESET
    
    project_files_id = []
    asset_data_model = await AssetDataModel.initialize_asset_model(db_client=db)
    if process_request.FILE_ID is not None:
        file_name = process_request.FILE_ID
        asset_file = await asset_data_model.get_asset_by_project_id_file_name(asset_file_name= file_name, asset_project_id= project.id)
        if asset_file is None:
            return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST,
                                content={
                                    "response signal": ResponseSignal.FILE_NOT_FOUND.value})
        project_files_id.append(asset_file) 
    
    else:
        project_files_id = await asset_data_model.get_assets_by_project_id(project_id= project.id,
                                                                     asset_type= AssetTypeEnum.FILE.value )
    
    
    if len(project_files_id) == 0:
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST,
    content={
        "response signal": ResponseSignal.PROJECT_IS_EMPYT.value,
        
    })
    
    if do_reset:
        _ = await chunk_data_model.delete_chunks_py_project_id(project_id=project.id)
         
    number_of_inserted_chunks = 0
    number_of_files = 0
    for file in project_files_id:
        file_id = file.asset_name
        file_content = process_controller.get_file_content(file_id= file_id)
        
        if file_content is None:
            logger.error(f"error in processing file with file id =  {file_id}, file my not be found in the system")
            continue
        #spltting file content to chunks
        
        file_chunks = process_controller.split_file_content(file_content=file_content,
                                                            chunk_size=chunk_size,
                                                            overlap=overlap)
        if len(file_chunks) == 0 or file_chunks == None:
            return JSONResponse(
                content={"response signal": ResponseSignal.FILE_PROCESSING_FALIED.value},
                status_code= status.HTTP_400_BAD_REQUEST
            )
        
        file_chunks_records = [DataChunk(
                                chunk_text=chunk.page_content,
                                chunk_meta_data=chunk.metadata,
                                chunk_project_id=project.id,
                                chunk_asset_id=file.id,
                                chunk_order=i + 1
                                ) 
                                for i, chunk in enumerate(file_chunks)
                                ]
        
        
        
        number_of_inserted_chunks += await chunk_data_model.insert_many_batches(chunks=file_chunks_records)
        number_of_files += 1
    
    return JSONResponse(
    content={
        "response signal": ResponseSignal.FILE_PROCESSING_SUCCEED.value,
        "number of inserted chunks" : number_of_inserted_chunks,
        "number of processed files": number_of_files
    })

    #return file_chunks