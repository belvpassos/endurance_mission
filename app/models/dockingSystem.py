import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from app.database import Base
from datetime import datetime

class DockingStatus (enum.Enum):
    UNDOCKED = "undocked"
    DOCKING = "docking"
    DOCKED = "docked"
    FAILED = "failed"
    
class DockingSystem(Base):
    __tablename__ = "docking_system"
    
    id = Column(Integer, primary_key=True, index=True)
    
    target_module = Column(String)
    status = Column(Enum(DockingStatus), default=DockingStatus.UNDOCKED)
    initiated_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    success = Column(Boolean, default=False)
    error_message = Column(String, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))