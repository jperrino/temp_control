from .base_model import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Measure(Base):
    __tablename__ = "measure"
    id = Column(Integer, primary_key=True, nullable=False)
    temperature = Column(Float, nullable=False)
    device = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP()'))
