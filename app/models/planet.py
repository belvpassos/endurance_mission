from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.database import Base


class Planet(Base):
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    type = Column(String, nullable=False)
    distance_from_earth_km = Column(Float, nullable=False)
    has_life = Column(Boolean, default=False)
    surface_temperature = Column(Float, nullable=True)
    discovered_by = Column(String, nullable=True)
    discovery_date = Column(Date, nullable=True)
    gravity = Column(Float, nullable=True)
    atmosphere = Column(String, nullable=True)
    habitability_score = Column(Float, nullable=True)
