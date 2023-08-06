from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import db_settings

'''
    DATABASE CONFIGURATION
'''
DB_USERNAME = db_settings.database_username
DB_PASSWORD = db_settings.database_password
DB_HOST = db_settings.database_hostname
DB_PORT = db_settings.database_port
DB_NAME = db_settings.database_name

SQL_ALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}' \
                           f'@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
