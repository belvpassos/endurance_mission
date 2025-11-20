# app/models/spacecraftStatus.py

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SpacecraftStatus(Base):
    __tablename__ = "spacecraft_status"

    id = Column(Integer, primary_key=True, index=True)
    
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    fuel_level = Column(Float, nullable=False)
    oxygen_level = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)

    is_operational = Column(Boolean, nullable=False, default=True)
    life_support_active = Column(Boolean, nullable=False, default=True)
    communication_active = Column(Boolean, nullable=False, default=True)

    mission = relationship("Mission", back_populates="spacecraft_status")
