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

class LifeSupportSystemUpdate(BaseModel):
    oxygen_level: Optional[float] = None
    co2_level: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    temperature: Optional[float] = None
    is_operational: Optional[bool] = None
    spacecraft_id: Optional[int] = None

class LifeSupportSystemOut(LifeSupportSystemBase):
    id: int
    is_operational: bool

    class Config:
        orm_mode = True
