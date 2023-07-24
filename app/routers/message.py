from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm import Session
from app.database.connection import get_db
from datetime import datetime
from app.chat import session_handler, messenger
from app.chat.flow_status import FlowStatus


router = APIRouter(
    prefix="/message",
    tags=['Message']
)


@router.post("/", status_code=status.HTTP_200_OK)
async def process_message(request: Request, db: Session = Depends(get_db)):
    message_data = await request.form()
    sender_number = message_data["From"]
    message_body = message_data["Body"]

    now = datetime.today()
    session = session_handler.get_session(sender_number, now, db)
    # session = None
    # flow_status = None

    # if not result:
    #     print("Session not found")
    # else:
    #     print("Session:")
    #     print(result.session)
    #     session = result[0]
    #     flow_status = result[1]
    #     print(session)
    #     print(flow_status)
    #     print("Session device:")
    #     print(session.chat_session_device)
    #     print("Session flow:")
    #     print(session.chat_session_flow)

    if not session or session.flow_id == FlowStatus.COMPLETED:
        session_handler.init_session(sender_number, now, db)
        messenger.send_welcome_message(sender_number)
    else:
        if not session.device:
            if not session_handler.get_device(message_body, db):
                messenger.send_device_not_found_message(sender_number, message_body)
            else:
                session_handler.update_session(sender_number, 'device', message_body, now, db)
                messenger.send_select_flow_message(sender_number)
            # messenger.send_device_not_found_message(sender_number, message_body)
        # if message_body.startswith('test'):
        #     session_handler.update_session(sender_number, message_body, now, db)
        #     messenger.send_select_time_range_message(sender_number)
        else:
            if session.flow_id == FlowStatus.STARTED:
                if message_body == "1":
                    session_handler.update_session(sender_number, 'flow', FlowStatus.REQUEST_GRAPH.value, now, db)
                    messenger.send_select_time_range_message(sender_number)
                if message_body == "2":
                    session_handler.update_session(sender_number, 'flow', FlowStatus.SET_MIN_TEMPERATURE.value, now, db)
                    messenger.send_select_temperature_min_message(sender_number)
            else:
                if session.flow_id == FlowStatus.REQUEST_GRAPH:
                    # session_handler.update_session(sender_number, 'step', 'graph_select', now, db)
                    messenger.process_graph_request_message(sender_number, session.device, message_body, db)
                    session_handler.update_session(sender_number, 'flow', FlowStatus.COMPLETED.value, now, db)
                    messenger.send_complete_flow_message(sender_number)
                elif session.flow_id == FlowStatus.SET_MIN_TEMPERATURE:
                    # print('set min temp')
                    # print(session.flow_id)
                    messenger.process_temp_set_message(session.device, session.flow_id, message_body, db)
                    # session_handler.update_session(sender_number, 'step', 'set_max_temp', now, db)
                    session_handler.update_session(sender_number, 'flow', FlowStatus.SET_MAX_TEMPERATURE.value, now, db)
                    messenger.send_select_temperature_max_message(sender_number)
                elif session.flow_id == FlowStatus.SET_MAX_TEMPERATURE:
                    # print('set max temp')
                    # print(session.flow_id)
                    messenger.process_temp_set_message(session.device, session.flow_id, message_body, db)
                    # TODO: make request to update Arduino temperature range
                    session_handler.update_session(sender_number, 'flow', FlowStatus.COMPLETED.value, now, db)
                    messenger.send_complete_flow_message(sender_number)
            # messenger.send_select_time_range_message(sender_number)
            # session = session_handler.get_session(sender_number, now, db)
