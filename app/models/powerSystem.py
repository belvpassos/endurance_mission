from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class powerSystem(Base):
    __tablename__ = "power_system"
    
    id = Column(Integer, primary_key=True, index=True)
    battery_level = Column(Float)
    solar_panel_status = Column(String)
    power_consumption = Column(Float)
    power_generation = Column(Float)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))