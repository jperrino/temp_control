from pydantic import BaseModel
from datetime import datetime


class GraphResponse(BaseModel):
    device: str
    file_path: str
    created_at: str
