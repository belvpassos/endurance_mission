from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.database import Base

class PowerSystem(Base):  # PascalCase — nome da classe deve começar com maiúscula
    __tablename__ = "power_system"
    
    id = Column(Integer, primary_key=True, index=True)
    battery_level = Column(Float, nullable=False)
    solar_panel_status = Column(String, nullable=False)
    power_consumption = Column(Float, nullable=False)
    power_generation = Column(Float, nullable=False)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
