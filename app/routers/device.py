from fastapi import APIRouter, status, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.routers.schemas import device as device_schema
from app.database.models import device as device_model
from app.database.connection import get_db

router = APIRouter(
    prefix="/device",
    tags=['Device']
)


@router.get("/", status_code=status.HTTP_201_CREATED, response_model=device_schema.DeviceResponse)
async def register_device(db: Session = Depends(get_db),
                          name: str = 'aaa'):
    found_device = db.query(device_model.Device).filter(device_model.Device.name == name).first()
    # found_device = device_query.first()

    if found_device:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Device {name} was already registered')
    new_device_to_db = device_model.Device(name=name)
    db.add(new_device_to_db)
    db.commit()
    db.refresh(new_device_to_db)
    return new_device_to_db
