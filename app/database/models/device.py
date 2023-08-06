from app.database.models.base_model import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP()'))
    temp_range_min = Column(Float, nullable=True)
    temp_range_max = Column(Float, nullable=True)
