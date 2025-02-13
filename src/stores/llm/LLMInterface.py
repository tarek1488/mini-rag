from abc import ABC, abstractmethod

class LLMInetrface(ABC):
    
    @abstractmethod
    def set_generagtion_model(self, model_id:str):
        pass
    
    @abstractmethod
    def set_embedding_model(self, model_id:str):
        pass
    
    @abstractmethod
    def generate_text(self, prompt:str, max_output_token: int, temprature: float):
        pass
    
    @abstractmethod
    def embed_text(self, text:str, document_type:str ,embedding_dimension: int):
        pass
    
    @abstractmethod
    def construct_prompt(self, prompt:str, role:str):
        pass
        
