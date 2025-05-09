from sqlalchemy import Column, Float, DateTime, Integer, ForeignKey, Boolean
from app.database import Base
from datetime import datetime

class ResourceManager(Base):
    __tablename__ = "resource_manager"
    
    id = Column(Integer, primary_key=True, index=True)
    
    power_avaliable = Column(Float)
    fuel_remaining = Column(Float)
    water_reserve = Column(Float)
    oxygen_level = Column(Float)
    co2_level = Column(Float)
    food_suplies = Column(Float)
    
    average_consuption_rate = Column(Float)
    projected_depletion_date = Column(DateTime)
    
    power_critical = Column(Boolean, default=False)
    fuel_critical = Column(Boolean, default=False)
    water_critical = Column(Boolean, default=False)
    oxygen_critical = Column(Boolean, default=False)
    food_critical = Column(Boolean, default=False)
    
    last_uupdate = Column(DateTime, default=datetime.utcnow)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))