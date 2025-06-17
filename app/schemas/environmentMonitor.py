from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EnvironmentMonitorBase(BaseException):
    internal_pressure: Optional[float]
    external_pressure: Optional[float]
    co2_level: Optional[float]
    o2_level: Optional[float]
    radiation_level: Optional[float]
    magnetic_field_strength: Optional[float]
    timestamp: Optional[datetime] = None
    
class EnvironmentoMonitorCreate(EnvironmentMonitorBase):
    pass

class EnvironmentMonitorUpdate(EnvironmentMonitorBase):
    pass

class EnvironmentMonitorInDB(EnvironmentMonitorBase):
    id: int
    spacecraft_id: int 
    timestamp: datetime
    
    class Config:
        from_attributes = True
    