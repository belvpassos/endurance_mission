from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey
from app.database import Base
from datetime import datetime

class GroundControlLog(Base):
    __tablename__ = "ground_control_log"
    
    id = Column(Integer, primary_key=True, index=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender = Column(String)
    receiver = Column(String)
    message_type = Column(String)
    content = Column(String)
    acknowledged = Column(Boolean)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))