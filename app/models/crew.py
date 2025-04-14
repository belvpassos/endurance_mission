from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Crew(Base):
    __tablename__ = "crew"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    
    mission = relationship("Mission", back_populates="crew_members")
