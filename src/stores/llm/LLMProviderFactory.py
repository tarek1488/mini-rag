from .LLMProviderEnum import LLMProviderEnum
from .providers import CoHereProvider, OpenAIProvider

class LLMProviderFactory:
    
    def __init__(self, config: dict):
        self.config = config
    
    def intialize_provider(self, provider_name: str):
        
        if provider_name == LLMProviderEnum.OPENAI.value:
            provider = OpenAIProvider(
                api_key= self.config.OPENAI_API_KEY,
                api_url= self.config.OPENAI_API_URL,
                default_input_max_characters= self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_output_max_token= self.config.GENERATION_DEFAULT_MAX_OUTPUT_TOKENS,
                model_temprature= self.config.GENERATION_DEFAULT_TEMPRATURE
            )
            return provider
        
        if provider_name == LLMProviderEnum.COHERE.value:
            provider = CoHereProvider(
                api_key= self.config.COHERE_API_KEY,
                default_input_max_characters= self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_output_max_token= self.config.GENERATION_DEFAULT_MAX_OUTPUT_TOKENS,
                model_temprature= self.config.GENERATION_DEFAULT_TEMPRATURE
            )
            return provider
        
        return None