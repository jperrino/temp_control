from twilio.rest import Client
from app.config import common_settings
from app.chat import processor
from sqlalchemy.orm import Session
from app.chat.message import Message

'''
    TWILIO CONFIGURATION
'''
TWILIO_ACCOUNT_SID = common_settings.twilio_account_sid
TWILIO_AUTH_TOKEN = common_settings.twilio_auth_token
TWILIO_PHONE_NUMBER = common_settings.twilio_phone_number


def send_welcome_message(phone_number: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.WELCOME_MESSAGE
    )


def send_select_time_range_message(phone_number: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.SELECT_TIME_RANGE_MESSAGE
    )


def send_select_temperature_max_message(phone_number: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.SELECT_TEMP_MAX_MESSAGE
    )


def send_select_temperature_min_message(phone_number: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.SELECT_TEMP_MIN_MESSAGE
    )


def send_select_flow_message(phone_number: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.SELECT_FLOW_MESSAGE
    )


def send_invalid_flow_option(phone_number: str, flow_option: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.INVALID_FLOW_OPTION_MESSAGE.replace('{flow_option}', flow_option)
    )


def send_device_not_found_message(phone_number: str, device: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.DEVICE_NOT_FOUND_MESSAGE.replace('{device}', device)
    )


def send_complete_flow_message(phone_number: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=Message.TRANSACTION_COMPLETED_MESSAGE
    )


def send_message(phone_number: str, content: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=content
    )


def process_graph_request_message(phone_number: str, device_name: str, time_range: str, db: Session):
    response = processor.get_graph(device_name, time_range, db)
    send_message(phone_number, response)


def process_temp_set_message(phone_number: str, device_name: str, flow_status: int, temp_value: str, db: Session):
    response = processor.set_temperature(device_name, flow_status, temp_value, db)
    if response is not None:
        send_message(phone_number, response)
        return False
    else:
        return True
