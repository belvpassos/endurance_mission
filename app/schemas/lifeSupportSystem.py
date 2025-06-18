from pydantic import BaseModel
from typing import Optional

class LifeSupportSystemBase(BaseModel):
    oxygen_level: float
    co2_level: float
    humidity: float
    pressure: float
    temperature: float
    spacecraft_id: int
    
class LifeSupportSystemCreate(LifeSupportSystemBase):
    pass

class LifeSupportSystemOut(LifeSupportSystemBase):
    id: int
    
    class Config:
        from_attribute = True