from ..LLMInterface import LLMInetrface
from openai import OpenAI
from logging import getLogger
from ..LLMRoleEnum import LLMRoleOpenAIEnum
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
        
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def set_generagtion_model(self, model_id:str):
        self.generation_model_id = model_id
        
    
    def set_embedding_model(self, model_id:str, vector_size:int):
        self.embedding_model_id = model_id
        self.embedding_vector_size = vector_size
        
    def generate_text(self, prompt:str, max_output_token: int = None, temprature: float= None, chat_history: list = []):
        if not self.client or self.client is None:
            self.logger.error("OpenAI client was not set")
            return None
        
        if self.generation_model_id is None:
            self.logger.error("Generation model id for OpenAI was not set")
            return None
        
        max_output_token = max_output_token if max_output_token is not None else self.default_output_max_token
        temprature = temprature if temprature is not None else self.model_temprature
        
        new_prompt = self.construct_prompt(prompt=prompt, role= LLMRoleOpenAIEnum.USER.value)
        
        chat_history.append(new_prompt)
        
        response = self.client.chat.completions.create(
            model= self.generation_model_id,
            messages= chat_history,
            max_output_token = max_output_token,
            temperature= temprature
        ) 
        
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error in chat completetion with OpenAI model")
            return None
            
        return response.choices[0].message["content"]
    
    
    def embed_text(self, text:str, document_type:str ,embedding_dimension: int):
        
        if not self.client or self.client is None:
            self.logger.error("OpenAI client was not set")
            return None
        
        if self.embedding_model_id is None:
            self.logger.error("Embedding model id for OpenAI was not set")
            return None
        response = self.client.embeddings.create(
            input= text,
            model= self.embedding_model_id,
            
        )
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while text embedding with OpenAI")
            return None
        
        return response.data[0].embedding
    
    
    def construct_prompt(self, prompt:str, role:str):
        constructed_prompt = {"role" : role, "content": self.process_text(text=prompt)}
        return constructed_prompt