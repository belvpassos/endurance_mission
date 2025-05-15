import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from app.database import Base

class EventType(enum.Enum):
    STAGE_SEPARATION = "stage_separation"
    ENGINE_BURN = "engine_burn"
    ORBITAL_INSERTION = "orbital_insertion"


class MissionEvent(Base):
    __tablename__ = "mission_events"
    
    id = Column(Integer, primary_key=True, index=False)
    event_type = Column(Enum(EventType), nullable=False)
    timestamp = Column(DateTime)
    description = Column(String)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))