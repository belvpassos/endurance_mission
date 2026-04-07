from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Spacecraft(Base):
    __tablename__ = "spacecraft"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True, index=True)
    registry_code = Column(String(60), nullable=False, unique=True, index=True)
    vehicle_class = Column(String(80), nullable=False)
    manufacturer = Column(String(120), nullable=True)
    status = Column(String(60), nullable=False, default="operational")
    mission_profile = Column(String(255), nullable=True)
    home_base = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    abort_systems = relationship("AbortRecoverySystem", back_populates="spacecraft")
    alerts = relationship("AlertSystem", back_populates="spacecraft")
    data_records = relationship("DataRecorder", back_populates="spacecraft")
    health_checks = relationship("SystemHealthCheck", back_populates="spacecraft")
