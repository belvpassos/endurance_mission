import enum
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from app.database import Base

class CoolingSystemStatus(enum.Enum):
    ON = "on"
    OFF = "off"
    ERROR = "error"

class ThermalControlSystem(Base):
    __tablename__ = "thermal_control_system"
    
    id = Column(Integer, primary_key=True, index=True)
    internal_temperature = Column(Float)
    external_temperature = Column(Float)
    cooling_system_status = Column(enum(CoolingSystemStatus), nullable=False)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))