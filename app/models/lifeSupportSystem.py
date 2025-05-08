from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from app.database import Base

class LifeSupportSystem(Base):
    __tablename__ = "life_support_system"
    
    id = Column(Integer, primary_key=True, index=True)
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
    
    oxygen_level = Column(Float, nullable=False)
    co2_level = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    
    is_operatonal = Column(Boolean, nullable=False, default=True)