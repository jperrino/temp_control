from app.database.models import session as chat_session_model, device as device_model, flow as flow_model
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.config import common_settings
from app.chat.flow_status import FlowStatus

'''
    SESSION CONFIGURATION
'''
SESSION_TIMEOUT = common_settings.session_time_minutes


def get_session(phone_num: str, session_time: datetime, db: Session):
    query = db.query(chat_session_model.Session)\
        .filter(
        chat_session_model.Session.phone_number == phone_num,
        chat_session_model.Session.end_time > session_time,
        chat_session_model.Session.flow_id != FlowStatus.COMPLETED
        )
    return query.first()


def init_session(phone_num: str, session_time: datetime, db: Session):
    session_end_time = session_time + timedelta(minutes=SESSION_TIMEOUT)
    new_session = chat_session_model.Session(phone_number=phone_num,
                                             end_time=session_end_time,
                                             flow_id=FlowStatus.STARTED.value)
    db.add(new_session)
    db.commit()
    # db.flush()


def get_device(device_name: str, db: Session):
    query = db.query(device_model.Device).filter(
        device_model.Device.name == device_name
    )
    return query.first()


def update_session(phone_num: str, field: str, value, session_time: datetime, db: Session):
    session = get_session(phone_num, session_time, db)
    if field == 'device':
        setattr(session, 'device', value)
    if field == 'flow':
        setattr(session, 'flow_id', value)
    db.commit()
    # db.flush()
