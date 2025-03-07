from fastapi import FastAPI , APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
import logging
from .schemes import PushRequest
from models import ProjectDataModel, ChunkDataModel
from models import ResponseSignal
from controllers import NLPController

logger = logging.getLogger('uvicorn.error')

nlp_router =  APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
)

@nlp_router.post("/index/push/{project_id}")
async def push_project_chunks_to_vectordb(request: Request, project_id: str, push_request: PushRequest):
    
    vector_db_client =  request.app.vector_db_client
    mongo_db_client = request.app.mongo_db
    
    project_data_model = await ProjectDataModel.initialize_project_model(db_client= mongo_db_client)
    
    project = await project_data_model.get_or_create_project(project_id= project_id)
    
    if not project:
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST,
                            content={"signal": ResponseSignal.PROJECT_NOT_FOUND.value})
    
    nlp_controller = NLPController(vector_db_client= vector_db_client,
                                   generation_backend_client= request.app.generation_client,
                                   embedding_backend_client=request.app.embedding_client)
    
    chunk_data_model =  await ChunkDataModel.initialize_chunk_model(db_client= mongo_db_client)
    
    page_num = 1
    inserted_item_count = 0
    idx = 0
    while True:
        
        page_chunks = await chunk_data_model.get_all_chunks(project_id= project.id, page_num= page_num)
        if page_chunks:
            page_num = page_num + 1
        else:
            break
        record_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)
        
        is_inserted = nlp_controller.psuh_data_into_vector_db(project=project,
                                                    chunks= page_chunks,
                                                    chunk_ids= record_ids,
                                                    do_reset= push_request.do_reset)
        if not is_inserted or is_inserted == None:
            return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST,
                            content={"signal": ResponseSignal.DATA_INSERTION_IN_VECTORDB_ERROR.value})
        inserted_item_count += len(page_chunks)
    
    return JSONResponse(status_code= status.HTTP_200_OK,
                        content={"signal": ResponseSignal.DATA_INSERTION_IN_VECTORDB_SUCCEED.value,
                                 "inserted_item_count": inserted_item_count})
            
    
    

@nlp_router.get("/index/info/{project_id}")
async def get_project_info_from_vectordb(request: Request, project_id: str):
    vector_db_client =  request.app.vector_db_client
    mongo_db_client = request.app.mongo_db
    
    project_data_model = await ProjectDataModel.initialize_project_model(db_client= mongo_db_client)
    
    project = await project_data_model.get_or_create_project(project_id= project_id)
    if not project:
        return JSONResponse(status_code= status.HTTP_400_BAD_REQUEST,
                            content={"signal": ResponseSignal.PROJECT_NOT_FOUND.value})
    
    nlp_controller = NLPController(vector_db_client= vector_db_client,
                                   generation_backend_client= request.app.generation_client,
                                   embedding_backend_client=request.app.embedding_client)
    

@nlp_router.get("/search_project/{project_id}")
async def search_project_by_vector():
    pass