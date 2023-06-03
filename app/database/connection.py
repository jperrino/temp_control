from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import settings

# SQL_ALCHEMY_DATABASE_URL = f'mysql+pymysql://admin:admin' \
#                            f'@localhost:3306/temp_control'

SQL_ALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.database_username}:{settings.database_password}' \
                           f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
