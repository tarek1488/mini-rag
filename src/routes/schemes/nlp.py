from pydantic_settings import BaseSettings
from typing import Optional

class PushRequest(BaseSettings):
    do_reset : Optional[int] = 0
    