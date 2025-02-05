from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    
    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int
    
    MONGO_DB_URL: str 
    MONGO_DB_DATABASE: str
    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()    