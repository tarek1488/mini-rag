from ..LLMInterface import LLMInetrface
from openai import OpenAI
from logging import getLogger
class OpenAIProvider(LLMInetrface):
    
    def __init__(self, api_key: str, api_url:str =None, default_input_max_characters:int = 1000,
                 default_output_max_token:int = 1000, model_temprature:float = 0.1 ):
        
        self.api_key = api_key
        self.api_url = api_url
        
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_token = default_output_max_token
        self.model_temprature = model_temprature
        
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_vector_size = None
        
        self.client = OpenAI(api_key= self.api_key, api_url= self.api_url)
        
        self.logger =  getLogger(__name__)
        
    
    def set_generagtion_model(self, model_id:str):
        pass