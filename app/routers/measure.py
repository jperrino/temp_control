from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routers.schemas import measure as measure_schema
from app.database.models import measure as measure_model
from app.database.models import device as device_model
from app.database.connection import get_db
import requests

router = APIRouter(
    prefix="/measure",
    tags=['Measure']
)


@router.get("/", status_code=status.HTTP_201_CREATED)
# , response_model=measure_schema.MeasureResponse)
async def get_measure(db: Session = Depends(get_db),
                      temp: float = 0,
                      device: str = 'default'):
    print(f"Temperature: {temp}, Device: {device}")

    found_device = db.query(device_model.Device).filter(device_model.Device.name == device).first()

    if not found_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Device {device} is not registered')

    new_measure_to_db = measure_model.Measure(temperature=temp, device_id=found_device.id)
    db.add(new_measure_to_db)
    db.commit()
    # retrieve recently created measure and store it in new_measure_to_db variable
    db.refresh(new_measure_to_db)
    # parse measure to dictionary and add max and min temperature ranges
    measure_response = new_measure_to_db.to_dict()
    measure_response['temp_range_max'] = found_device.temp_range_max
    measure_response['temp_range_min'] = found_device.temp_range_min
    return measure_response
