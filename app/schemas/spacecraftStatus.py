from pydantic import BaseModel
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

class SpacecraftStatusResponse(SpacecraftStatusBase):
    id: int

    class Config:
        orm_mode = True