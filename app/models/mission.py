from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relacionamentos
    crew_members = relationship("Crew", back_populates="mission", cascade="all, delete-orphan")
    telemetry_data = relationship("Telemetry", back_populates="mission", cascade="all, delete-orphan")
    spacecraft_status = relationship("SpacecraftStatus", back_populates="mission", cascade="all, delete-orphan")
