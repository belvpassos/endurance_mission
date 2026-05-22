from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class MissionPhase(str, Enum):
    PRELAUNCH = "prelaunch"
    ASCENT = "ascent"
    ORBITAL_OPERATIONS = "orbital_operations"
    TRANSFER = "transfer"
    APPROACH = "approach"
    LANDING = "landing"
    SURFACE_OPERATIONS = "surface_operations"

class MissionBase(BaseModel):
    name: str
    status: str
    phase: MissionPhase = MissionPhase.PRELAUNCH
    start_time: Optional[datetime] = None  # deixa opcional para criar sem passar

class MissionCreate(MissionBase):
    pass

class MissionUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    phase: Optional[MissionPhase] = None
    start_time: Optional[datetime] = None

class Mission(MissionBase):
    id: int

    class Config:
        from_attributes = True
