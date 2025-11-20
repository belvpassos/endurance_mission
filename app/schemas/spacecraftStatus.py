# app/schemas/spacecraftStatus.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SpacecraftStatusBase(BaseModel):
    timestamp: datetime
    fuel_level: float
    oxygen_level: float
    temperature: float
    pressure: float
    is_operational: bool
    life_support_active: bool
    communication_active: bool
    mission_id: int

class SpacecraftStatusCreate(SpacecraftStatusBase):
    pass

class SpacecraftStatusUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    fuel_level: Optional[float] = None
    oxygen_level: Optional[float] = None
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    is_operational: Optional[bool] = None
    life_support_active: Optional[bool] = None
    communication_active: Optional[bool] = None
    mission_id: Optional[int] = None

class SpacecraftStatusResponse(SpacecraftStatusBase):
    id: int

    class Config:
        from_attributes = True
