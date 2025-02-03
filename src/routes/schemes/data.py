from pydantic_settings import BaseSettings
from typing import Optional

class ProcessRequest(BaseSettings):
    FILE_ID : str
    CHUNK_SIZE: Optional[int]= 100
    OVERLAP: Optional[int] = 20 
    DO_RESET: Optional[int] = 0  