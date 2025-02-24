from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True)

    # Define relationship to Plate
    plates = relationship("Plate", back_populates="owner")

class Plate(Base):
    __tablename__ = 'plates'

    id = Column(Integer, primary_key=True)
    plate_number = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="plates")
    alerts = relationship("Alert", back_populates="plate")

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True)
    plate_id = Column(Integer, ForeignKey('plates.id'), nullable=False)
    mentioned_by = Column(Integer, nullable=False)  # Assuming it stores a user ID
    chat_id = Column(Integer, nullable=False)  # Assuming it stores a chat ID
    mentioned_at = Column(DateTime, nullable=False)

    plate = relationship("Plate", back_populates="alerts")