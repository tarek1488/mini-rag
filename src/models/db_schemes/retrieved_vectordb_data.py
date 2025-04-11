from pydantic import BaseModel, Field, field_validator
from typing import Optional


class RetrievedVectorDBData(BaseModel):
    text: str
    score: float
    meta_data: Optional[dict]