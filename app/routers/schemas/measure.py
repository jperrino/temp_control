from pydantic import BaseModel
from datetime import datetime


class MeasureResponse(BaseModel):
    id: int
    temperature: float
    device_id: int
    created_at: datetime

    class Config:
        orm_mode = True
