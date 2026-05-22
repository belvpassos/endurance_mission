import enum
import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.database import Base


class MissionPhase(enum.Enum):
    PRELAUNCH = "prelaunch"
    ASCENT = "ascent"
    ORBITAL_OPERATIONS = "orbital_operations"
    TRANSFER = "transfer"
    APPROACH = "approach"
    LANDING = "landing"
    SURFACE_OPERATIONS = "surface_operations"


class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)
    phase = Column(
        SqlEnum(MissionPhase, values_callable=lambda enum_cls: [item.value for item in enum_cls], native_enum=False),
        nullable=False,
        default=MissionPhase.PRELAUNCH.value,
    )
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relacionamentos
    crew_members = relationship("Crew", back_populates="mission", cascade="all, delete-orphan")
    telemetry_data = relationship("Telemetry", back_populates="mission", cascade="all, delete-orphan")
    spacecraft_status = relationship("SpacecraftStatus", back_populates="mission", cascade="all, delete-orphan")
