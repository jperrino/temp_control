from pydantic import BaseSettings


class DataBaseSettings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str

    class Config:
        env_file = '.db_config_local'
        env_file_encoding = 'utf-8'


class CommonSettings(BaseSettings):
    app_host: str
    app_port: int
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    aws_access_key: str
    aws_secret_key: str
    aws_bucket_name: str
    aws_url: str
    session_time_minutes: int
    graphs_file_path: str

    class Config:
        env_file = '.common_config'
        env_file_encoding = 'utf-8'


db_settings = DataBaseSettings()
common_settings = CommonSettings()
