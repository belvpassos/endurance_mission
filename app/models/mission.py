from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    
    crew_members = relationship("Crew", back_populates="mission", cascade="all, delete")