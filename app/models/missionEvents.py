import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class EventType(enum.Enum):
    STAGE_SEPARATION = "stage_separation"
    ENGINE_BURN = "engine_burn"
    ORBITAL_INSERTION = "orbital_insertion"

class MissionEvent(Base):
    __tablename__ = "mission_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(Enum(EventType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
