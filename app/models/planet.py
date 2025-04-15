from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.database import Base

class Planet(Base):
    __tablename__ = "planets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    type = Column(String, nullable=False)
    distance_from_earth_km = Column(Float, nullable=False)
    has_life = Column(Boolean, default=False)
    surface_temperature = Column(Float)
    discovered_by = Column(String)
    discovery_date = Column(Date)
    gravity = Column(Float)
    atmosphere = Column(String)
    habitability_score = Column(Float)