from .providers import QdrantProvider
from .VectorDBEnums import VectorDBProviders
from controllers.BaseController import BaseController
class VectorDBFactory:
    
    def __init__(self, config: dict):
        self.config = config
        self.base_controller = BaseController()
        
    def intialize_provider(self, provider_name: str):
        
        if provider_name == VectorDBProviders.QDRANT.value:
            database_path = self.base_controller.get_vector_database_path(db_name = self.config.VECTORDB_PATH)
            provider = QdrantProvider(data_base_path= database_path, 
                                      distance_method= self.config.VECTORDB_DISTANCE_METHOD)
            return provider
        return None
            
    
    