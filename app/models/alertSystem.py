import enum
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Enum as SqlEnum
from app.database import Base
from datetime import datetime


class AlertType(enum.Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class AlertSystem(Base):
    __tablename__ = "alert_system"
    
    id = Column(Integer, primary_key=True, index=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    system = Column(String)
    alert_type = Column(SqlEnum(AlertType), nullable=False)
    message = Column(String)
    acknowledged = Column(Boolean, default=False)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))
