from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    GO_FOR_PROP_LOAD = "go_for_prop_load"
    PROP_LOAD_COMPLETE = "prop_load_complete"
    TERMINAL_COUNT = "terminal_count"
    COMMAND_UPLINK = "command_uplink"
    COMMAND_EXECUTING = "command_executing"
    COMMAND_CONFIRMED = "command_confirmed"
    COMMAND_FAILED = "command_failed"
    ENGINE_IGNITION = "engine_ignition"
    LIFTOFF = "liftoff"
    MAX_Q = "max_q"
    MECO = "meco"
    STAGE_SEPARATION = "stage_separation"
    ENGINE_BURN = "engine_burn"
    ORBITAL_INSERTION = "orbital_insertion"
    COURSE_CORRECTION_BURN = "course_correction_burn"
    DEORBIT_BURN = "deorbit_burn"
    ENTRY_INTERFACE = "entry_interface"
    LANDING_BURN = "landing_burn"
    SHIP_LANDING = "ship_landing"

class MissionEventBase(BaseModel):
    event_type: EventType
    timestamp: datetime
    description: Optional[str] = None

class MissionEventCreate(MissionEventBase):
    spacecraft_id: int

class MissionEventUpdate(BaseModel):
    event_type: Optional[EventType] = None
    timestamp: Optional[datetime] = None
    description: Optional[str] = None

class MissionEvent(MissionEventBase):
    id: int
    spacecraft_id: int

    class Config:
        from_attributes = True
