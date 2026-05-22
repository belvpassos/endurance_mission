import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class EventType(enum.Enum):
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

class MissionEvent(Base):
    __tablename__ = "mission_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(
        Enum(EventType, values_callable=lambda enum_cls: [item.value for item in enum_cls], native_enum=False),
        nullable=False,
    )
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
