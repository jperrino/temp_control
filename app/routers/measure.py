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


@router.get("/", status_code=status.HTTP_201_CREATED, response_model=measure_schema.MeasureResponse)
async def get_measure(db: Session = Depends(get_db),
                      temp: float = 0,
                      device: str = 'aaa'):
    print(f"Temperature: {temp}, Device: {device}")
    # measure = db.query(measure_model.Measure).first()

    # response = requests.get('https://httpbin.org/get')
    # print(response.json())

    # print(measure)
    # return {"message": "OK"}
    # return measure

    # new_measure = {"temperature": temp, "device": device}
    found_device = db.query(device_model.Device).filter(device_model.Device.name == device).first()
    # found_device = device_query.first()

    if not found_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Device {device} is not registered')

    new_measure_to_db = measure_model.Measure(temperature=temp, device_id=found_device.id)
    db.add(new_measure_to_db)
    db.commit()
    db.refresh(new_measure_to_db)  # retrieve recently created post and store it in new_post variable
    return new_measure_to_db

