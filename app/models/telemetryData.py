from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base   

class Telemetry(Base):
    __tablename__ = "telemetry_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
    position_z = Column(Float, nullable=False)

    velocity = Column(Float, nullable=False)
    acceleration = Column(Float, nullable=False)

    distance_from_earth = Column(Float, nullable=False)
    distance_to_target = Column(Float, nullable=False)

    orbital_status = Column(String, nullable=False)
    pitch = Column(Float, nullable=False)
    yaw = Column(Float, nullable=False)
    roll = Column(Float, nullable=False)

    mission = relationship("Mission", back_populates="telemetry_data")
