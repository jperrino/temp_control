from pydantic import BaseModel
from datetime import datetime


class GraphRequest(BaseModel):
    option: str


class GraphResponse(BaseModel):
    device: str
    file_path: str
    created_at: str
