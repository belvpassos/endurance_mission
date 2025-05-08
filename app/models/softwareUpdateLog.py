from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class SoftwareUpdateLog(Base):
    __tablename__ = "software_update_log"
    
    id = Column(Integer, primary_key=True, index=True)
    
    version = Column(String)
    update_type = Column(String)
    status = Column(String)
    initiated_by = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))
    
    