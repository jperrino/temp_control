from app.database.models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database.models.flow import Flow


class Session(Base):
    __tablename__ = "chat_session"
    id = Column(Integer, primary_key=True, nullable=False)
    phone_number = Column(String, nullable=False)
    device = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP()'))
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    flow_id = Column(Integer, ForeignKey('flow.id', ondelete='CASCADE'), nullable=False)
    flow = relationship('Flow')
