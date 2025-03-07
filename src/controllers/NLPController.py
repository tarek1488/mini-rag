from .BaseController import BaseController
from models.db_schemes import Project
from models.db_schemes import DataChunk
from typing import List
from stores.llm.DocumentTypeEnum import DocumentTypeEnum
class NLPController(BaseController):
    
    def __init__(self, vector_db_client, generation_backend_client, embedding_backend_client):
        super().__init__()
        
        self.vector_db_client = vector_db_client
        self.generation_backend_client = generation_backend_client
        self.embedding_backend_client = embedding_backend_client
    
    def create_collection_name(self, project_id:str):
        name =  f'collection_{project_id}'.strip()
        return name
    
    def reset_vector_db_collection(self, project: Project):
        
        collection_name =  self.create_collection_name(project_id= project.project_id)
        
        return self.vector_db_client.delete_collection(collection_name = collection_name)
    
    def get_vector_collection_info(self, project: Project):
        collection_name =  self.create_collection_name(project_id= project.project_id)
        return self.vector_db_client.get_collection(collection_name= collection_name)
    
    def psuh_data_into_vector_db(self, project: Project, chunks: List[DataChunk], do_reset: int = 0):
        
        #1-get collection name
        collection_name =  self.create_collection_name(project_id= project.project_id) 
        
        # #2-check if do reset == 1 delete the collection
        # if(do_reset):
        #     self.reset_vector_db_collection(project=  project)
        
        #3-process chunks
        texts = [chunk.chunk_text for chunk in chunks]
        meta_datas = [chunk.chunk_meta_data for chunk in chunks]
        vectors = [self.embedding_backend_client.embed_text( text = text,
                                                           document_type = DocumentTypeEnum.DOCUMENT.value)
                  for text in texts]
        
        #4-create collection
        return_val = self.vector_db_client.create_collection(collection_name = collection_name,
                                                embedding_size = self.app_settings.EMBEDDING_MODEL_SIZE,
                                                do_reset = do_reset)
        if return_val is None:
            return None
        
        
        #5-insert push data to vector db
        return_val = self.vector_db_client.insert_many_records(collection_name= collection_name,
                                                  texts = texts,
                                                  vectors= vectors ,
                                                  meta_datas = meta_datas,)
        if return_val != True:
            return None
        
        
        return True
        