from pydantic import BaseModel
from datetime import datetime


class DeviceResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True
