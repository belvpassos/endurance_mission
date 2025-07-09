from pydantic import BaseModel
from typing import Optional

class PowerSystemBase(BaseModel):
    battery_level: float
    solar_panel_status: str
    power_consumption: float
    power_generation: float 
    
class PowerSystemCreate(PowerSystemBase):
    spacecraft_id: int
    
class PowerSystemUpdate(PowerSystemBase):
    battery_level: Optional[float] = None
    solar_panel_status: Optional[str] = None
    power_consumption: Optional[float] = None
    power_generation: Optional[float] = None
    
    
class PowerSystem(PowerSystemBase):
    id: int
    spacecraft_id: int
    
    class Config:
        from_attributes: True
    