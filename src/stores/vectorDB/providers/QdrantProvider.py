from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import VectorDBMetricMethod
from logging import Logger
from qdrant_client import QdrantClient, models


class QdrantProvider(VectorDBInterface):
    def __init__(self, data_base_path: str, distance_method: str):
        
        if distance_method == VectorDBMetricMethod.COSINE.value:
            self.distance_method = models.Distance.COSINE
        
        elif distance_method == VectorDBMetricMethod.DOT.value:
            self.distance_method = models.Distance.DOT
        
        self.data_base_path = data_base_path
        
        self.client = None
        
        self.logger = Logger(__name__)
        
    # def validate_connection(self):
    #     if self.client is None or not self.client:
    #         return False
    #     return True
    
    
    def connect(self):
        self.client =  QdrantClient(path= self.data_base_path)
        
    
     
    def disconnect(self):
        self.client = None
    
     
    def get_collection(self, collection_name: str):
        collection = self.client.get_collection(collection_name= collection_name)
        
        if collection or collection is not None:
            return collection
        
        self.logger.info("There no such a collection exists with this name")
        return None 
        
    
     
    def get_all_collection(self):
        all_collections = self.client.get_collections()
        return all_collections
    
     
    def is_Collection_exists(self, collection_name: str):
        return self.client.collection_exists(collection_name= collection_name)
        
    
     
    def create_collection(self, collection_name: str, embedding_size: int , do_reset: bool = False):
        
        # if not self.validate_connection():
        #     self.logger.error("Error while connecting to Qdrant DB client")
        #     return None
        
        if do_reset:
            _ = self.delete_collection(collection_name= collection_name)
        
        if self.is_Collection_exists(collection_name= collection_name):
            self.logger.info("This collection is already exists ")
            return None
        
        _ = self.client.create_collection(collection_name= collection_name,
                                          vectors_config= models.VectorParams(size= embedding_size, distance=self.distance_method))
        return True

    
     
    def delete_collection(self, collection_name: str):
        
        if self.is_Collection_exists(collection_name= collection_name):
            return self.client.delete_collection(collection_name= collection_name)
        
        self.logger.info("There no such a collection exists with this name to be deleted")
            
    
     
    def insert_one_record(self, collection_name: str, text: str, vector: list,
                          meta_data: dict = None, record_id: int = None ):
        
        #check if collection exits or not
        if not self.is_Collection_exists(collection_name= collection_name):
            self.logger.error("There is no such a collection exits with this name")
            return None
        
        point =  models.PointStruct(
            id= [record_id],
            payload= {"text" : text, "metadata": meta_data},
            vector= vector
        )
        try:
            _ = self.client.upload_points(collection_name= collection_name,points=[point],)
        
        except Exception as e:
                self.logger.error(f"Error while inserting one record: {e}")
        
        return True
            
        
    def insert_many_records(self, collection_name: str, texts: list, vectors:list,
                            meta_datas: list = None, record_ids : list = None, batch_size: int = 50):
        
        #check if collection exits or not
        if not self.is_Collection_exists(collection_name= collection_name):
            self.logger.error("There is no such a collection exits with this name")
            return None
        
        if meta_datas is None:
            meta_datas = [None] * len(texts)
        
        if record_ids is None:
            record_ids  = list(range(0, len(texts)))
        
        points = []
        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size
            
            batch_texts = texts[i : batch_end]
            batch_vectors = vectors[i : batch_end]
            batch_metadatas = meta_datas[i : batch_end]
            batch_record_ids =  record_ids[i : batch_end]
            
            batch_points = [
                models.PointStruct(id = batch_record_ids[j],
                    payload = {"text" : batch_texts[j], "metadata" : batch_metadatas[j]},
                    vector= batch_vectors[j]
                )
                for j in range(len(batch_texts))
            ]
            
            try:
                _ = self.client.upload_points(collection_name= collection_name, points=batch_points)
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
        
        return True
        
    
     
    def search_by_vector(self, collection_name: str, vector: list, limit:int = 3):
        return self.client.search(collection_name= collection_name,
                                  query_vector= vector,
                                  limit=3)  
        
