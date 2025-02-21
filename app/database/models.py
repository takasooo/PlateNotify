from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plate(Base):
    __tablename__ = "plates"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    plate_number = Column(String, unique=True, nullable=False)
