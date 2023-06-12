from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    graphs_file_path: str

    class Config:
        env_file = '.env_remote'
        env_file_encoding = 'utf-8'


settings = Settings()
