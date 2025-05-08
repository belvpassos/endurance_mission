from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class EnvironmentMonitor(Base):
    __tablename__ = "environment_monitor"
    
    id = Column(Integer, primary_key=True, index=True)
    
    internal_pressure = Column(Float)
    external_pressure = Column(Float)
    co2_level = Column(Float)
    o2_level = Column(Float)
    radiation_level = Column(Float)
    magnetic_field_strength = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))