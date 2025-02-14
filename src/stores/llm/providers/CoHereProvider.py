from ..LLMInterface import LLMInetrface
from ..LLMInterface import LLMInetrface
from cohere import ClientV2
from logging import getLogger
from ..LLMRoleEnum import LLMRoleEnum

class CoHereProvider(LLMInetrface):
    def __init__(self, api_key: str, default_input_max_characters:int = 1000,
                 default_output_max_token:int = 1000, model_temprature:float = 0.1 ):
        
        self.api_key = api_key
        
        
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_token = default_output_max_token
        self.model_temprature = model_temprature
        
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_vector_size = None
        
        self.client = ClientV2(api_key= self.api_key)
        
        self.logger =  getLogger(__name__)
    
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def set_generagtion_model(self, model_id:str):
        self.generation_model_id = model_id
        
    
    def set_embedding_model(self, model_id:str, vector_size:int):
        self.embedding_model_id = model_id
        self.embedding_vector_size = vector_size
    
    def generate_text(self, prompt:str, max_output_token: int = None, temprature: float= None, chat_history: list = []):
        
        if not self.client or self.client is None:
            self.logger.error("Error while connecting to Cohere Client (Cohere client was not set)")
            return None
        
        if self.generation_model_id is None:
            self.logger.error("Generation model id for Cohere was not set")
            return None
        
        max_output_token = max_output_token if max_output_token is not None else self.default_output_max_token
        temprature = temprature if temprature is not None else self.model_temprature
        
        new_prompt = self.construct_prompt(prompt=prompt, role=LLMRoleEnum.USER.value)
        chat_history.append(new_prompt)
        
        response = self.client.chat(model= self.generation_model_id,
                                    temperature= temprature,
                                    max_output_token = max_output_token,
                                    messages=chat_history)
        
        if not response or not response.message or len(response.message.content) == 0 or not response.message.content[0].text:
            self.logger.error("Error in chat completetion with Cohere model")
            return None
        
        return response.message.content[0].text
            
        
    def embed_text(self, text:str, document_type:str ,embedding_dimension: int):
        pass
    
    def construct_prompt(self, prompt:str, role:str):
        constructed_prompt = {"role" : role, "content": self.process_text(text=prompt)}
        return constructed_prompt