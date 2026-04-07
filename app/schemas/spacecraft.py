from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SpacecraftBase(BaseModel):
    name: str
    registry_code: str
    vehicle_class: str
    manufacturer: Optional[str] = None
    status: str = "operational"
    mission_profile: Optional[str] = None
    home_base: Optional[str] = None


class SpacecraftCreate(SpacecraftBase):
    pass


class SpacecraftUpdate(BaseModel):
    name: Optional[str] = None
    registry_code: Optional[str] = None
    vehicle_class: Optional[str] = None
    manufacturer: Optional[str] = None
    status: Optional[str] = None
    mission_profile: Optional[str] = None
    home_base: Optional[str] = None


class Spacecraft(SpacecraftBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
