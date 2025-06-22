from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    STAGE_SEPARATION = "stage_separation"
    ENGINE_BURN = "engine_burn"
    ORBITAL_INSERTION = "orbital_insertion"
    

class MissionEventBase(BaseModel):
    event_type: EventType
    timestamp: datetime
    description: Optional[str] = None
    

class MissionEventCreate(MissionEventBase):
    spacecraft_id: int
    

class MissionEventUpdate(BaseModel):
    event_type: Optional[EventType] = None
    timestamp: Optional [datetime] = None
    description: Optional[str] = None
    
class MissionEvent(MissionEventBase):
    id: int
    spacecraft_id: int
    
    class Config:
        from_attributes = True