from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
import datetime

class SystemHealthCheck(Base):
    __tablename__ = "system_health_check"
    
    id = Column(Integer, primary_key=True, index=True)
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
    
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    system_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)