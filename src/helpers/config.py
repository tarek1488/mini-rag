from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    
    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int
    
    MONGO_DB_URL: str 
    MONGO_DB_DATABASE: str
    
    GENERATION_BACKEND: str = None
    EMBEDDING_BACKEND: str = None

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None

    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None 
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    GENERATION_DEFAULT_MAX_OUTPUT_TOKENS: int = None
    GENERATION_DEFAULT_TEMPRATURE:float = None
    INPUT_DEFAULT_MAX_CHARACTERS:int = None
    
    VECTORDB_PROVIDER: str = None
    VECTORDB_PATH: str = None
    VECTORDB_DISTANCE_METHOD: str = None
    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()    