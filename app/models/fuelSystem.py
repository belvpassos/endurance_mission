from sqlalchemy import Column, Float, Integer, ForeignKey
from app.database import Base

class Fuel(Base):
    __tablename__ = "fuel_system"
    
    id = Column(Integer, primary_key=True, index=True)
    fuel_level = Column(Float)
    fuel_consupmtion_level = Column(Float)
    fuel_temperature = Column(Float)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))