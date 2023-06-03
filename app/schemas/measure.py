from pydantic import BaseModel
from datetime import datetime

# class MeasureResponse(BaseModel):
#     message: str


class MeasureResponse(BaseModel):
    id: int
    temperature: int
    device: str
    created_at: datetime

    class Config:
        orm_mode = True
