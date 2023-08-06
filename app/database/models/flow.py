from app.database.models.base_model import Base
from sqlalchemy import Column, Integer, String


class Flow(Base):
    __tablename__ = "flow"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
