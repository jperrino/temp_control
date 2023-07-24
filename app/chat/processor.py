from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import cast, Date
from app.database.models import measure as measure_model
from app.database.models import device as device_model
from app.chat.message import Message
from app.chat.time_range import TimeRange
from app.plotting import plotter
from app.uploading import uploader
from app.chat.flow_status import FlowStatus

# '''
#     TIME RANGE
# '''
# TIME_RANGE = {"1": 'today',
#               "2": 'week',
#               "3": 'month'
#               }


def get_graph(device_name: str, time_range: str, db: Session):
    # time = TIME_RANGE.get(time_range)
    device = db.query(device_model.Device).filter(device_model.Device.name == device_name).first()
    dev_id = int(device.id)

    # https://stackoverflow.com/questions/38878897/how-to-make-a-subquery-in-sqlalchemy

    today_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    week_ago_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day - 7)
    month_ago_datetime = datetime(datetime.today().year, datetime.today().month - 1, datetime.today().day)

    if time_range == TimeRange.diaria:
        query = db.query(measure_model.Measure).filter(
                                            measure_model.Measure.device_id == dev_id,
                                            measure_model.Measure.created_at >= today_datetime
                                            )
        # query = db.query(measure_model.Measure).filter(
        #                                     measure_model.Measure.device == device,
        #                                     measure_model.Measure.created_at >= today_datetime
        #                                     )
    elif time_range == TimeRange.semanal:
        query = db.query(func.avg(measure_model.Measure.temperature).label('temperature'),
                         cast(measure_model.Measure.created_at, Date).label('created_at')
                         ).filter(
                            measure_model.Measure.device_id == dev_id,
                            measure_model.Measure.created_at >= week_ago_datetime
                            ).group_by(cast(measure_model.Measure.created_at, Date))
    elif time_range == TimeRange.mensual:
        query = db.query(func.avg(measure_model.Measure.temperature).label('temperature'),
                         cast(measure_model.Measure.created_at, Date).label('created_at')
                         ).filter(
                            measure_model.Measure.device_id == dev_id,
                            measure_model.Measure.created_at >= month_ago_datetime
                            ).group_by(cast(measure_model.Measure.created_at, Date))
        # query = db.query(measure_model.Measure).filter(
        #                                     measure_model.Measure.device_id == dev_id,
        #                                     measure_model.Measure.created_at >= month_ago_datetime
        #                                     )
    else:
        return Message.INVALID_TIME_RANGE_MESSAGE.replace('{time_range}', time_range)
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail=f"Invalid time: {time} was provided")

    # print("query:", query)
    measure_list = query.all()
    if not measure_list:
        return Message.RECORD_NOT_FOUND_MESSAGE.replace('{device}', device_name)
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"No temperature records found for device: {device}")

    # Create graph
    plot_result = plotter.plot_graph(measure_list, device_name)

    # Upload graph to S3 bucket
    # s3_file_name = plot_result['name'] + TimeRange(time_range).name
    s3_file_name = f"{TimeRange(time_range).name}_{plot_result['name']}"
    file_s3_url = uploader.upload_graph_to_s3_bucket(plot_result['path'], s3_file_name)

    message = Message.GRAPH_RESPONSE_MESSAGE\
        .replace('{time_range}', TimeRange(time_range).name)\
        .replace('{device}', device_name)\
        .replace('{graph_url}', file_s3_url)

    return message


def set_temperature(device_name: str, flow_status: int, temp_value: str, db: Session):
    temp_value = float(temp_value)
    device = db.query(device_model.Device).filter(device_model.Device.name == device_name).first()
    if flow_status == FlowStatus.SET_MIN_TEMPERATURE.value:
        setattr(device, 'temp_range_min', temp_value)
    if flow_status == FlowStatus.SET_MAX_TEMPERATURE.value:
        # TODO: si temp_value < device.temp_range_min : return error
        setattr(device, 'temp_range_max', temp_value)
    # if field == 'step':
    #     setattr(session, 'step', value)
    db.commit()


