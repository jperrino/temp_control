from app.database.models.base_model import Base
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database.models.device import Device


class Measure(Base):
    __tablename__ = "measure"
    id = Column(Integer, primary_key=True, nullable=False)
    temperature = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP()'))
    device_id = Column(Integer, ForeignKey('device.id', ondelete='CASCADE'), nullable=False)
    device = relationship('Device')

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
