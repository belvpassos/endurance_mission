from pydantic import BaseModel
from enum import Enum
from typing import Optional

class CoolingSystemStatusEnum(str, Enum):
    ON = "on"
    OFF = "off"
    ERROR = "error"

class ThermalControlSystemBase(BaseModel):
    internal_temperature: float
    external_temperature: float
    cooling_system_status: CoolingSystemStatusEnum
    spacecraft_id: int

class ThermalControlSystemCreate(ThermalControlSystemBase):
    pass

class ThermalControlSystemUpdate(BaseModel):
    internal_temperature: Optional[float] = None
    external_temperature: Optional[float] = None
    cooling_system_status: Optional[CoolingSystemStatusEnum] = None

class ThermalControlSystemResponse(ThermalControlSystemBase):
    id: int

    class Config:
        from_attributes = True
