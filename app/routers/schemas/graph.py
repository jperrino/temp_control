from pydantic import BaseModel


class GraphRequest(BaseModel):
    option: str


class GraphResponse(BaseModel):
    device: str
    file_path: str
    created_at: str
