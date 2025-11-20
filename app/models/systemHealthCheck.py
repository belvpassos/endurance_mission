from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class SystemHealthCheck(Base):
    __tablename__ = "system_health_check"
    
    id = Column(Integer, primary_key=True, index=True)
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
    
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    system_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    message = Column(String(1000), nullable=True)
    
    spacecraft = relationship("Spacecraft", back_populates="health_checks")
