from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SpacecraftStatus(Base):
    __tablename__="spacecraft_status"
    
    id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey('missions.id'), nullable=False)
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    fuel_level = Column(Float, nullable=False)
    oxygen_level = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    
    is_operational = Column(Boolean, nullable=False)
    life_support_active = Column(Boolean, nullable=False)
    communication_active = Column(Boolean, nullable=False)
    
    mission = relationship("Mission", back_populates="spacecraft_status")
