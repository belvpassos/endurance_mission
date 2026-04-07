from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EnvironmentMonitorBase(BaseModel):
    internal_pressure: Optional[float] = None
    external_pressure: Optional[float] = None
    co2_level: Optional[float] = None
    o2_level: Optional[float] = None
    radiation_level: Optional[float] = None
    magnetic_field_strength: Optional[float] = None
    timestamp: Optional[datetime] = None

class EnvironmentMonitorCreate(EnvironmentMonitorBase):
    spacecraft_id: int

class EnvironmentMonitorUpdate(EnvironmentMonitorBase):
    spacecraft_id: Optional[int] = None

class EnvironmentMonitorInDB(EnvironmentMonitorBase):
    id: int
    spacecraft_id: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
