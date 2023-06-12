from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import graph as graph_schema
from ..models import measure as measure_model
from ..database.connection import get_db
from datetime import datetime
from ..plotting import plotter

router = APIRouter(
    prefix="/graph",
    tags=['Graph']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=graph_schema.GraphResponse)
async def get_graph(db: Session = Depends(get_db),
                    device: str = 'aaa',
                    time: str = 'bbb'):
    today_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    week_ago_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day - 7)
    month_ago_datetime = datetime(datetime.today().year, datetime.today().month - 1, datetime.today().day)

    if time == 'today':
        query = db.query(measure_model.Measure).filter(
                                            measure_model.Measure.device == device,
                                            measure_model.Measure.created_at >= today_datetime
                                            )
    elif time == 'week':
        query = db.query(measure_model.Measure).filter(
                                            measure_model.Measure.device == device,
                                            measure_model.Measure.created_at >= week_ago_datetime
                                            )
    elif time == 'month':
        query = db.query(measure_model.Measure).filter(
                                            measure_model.Measure.device == device,
                                            measure_model.Measure.created_at >= month_ago_datetime
                                            )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid time: {time} was provided")

    # print("query:", query)
    measure_list = query.all()
    if not measure_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No temperature records found for device: {device}")

    plot_result = plotter.plot_graph(measure_list, device)

    return {"device": device, "file_path": plot_result['path'], "created_at": plot_result['time']}
