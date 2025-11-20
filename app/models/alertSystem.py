import enum
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class AlertType(enum.Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class AlertSystem(Base):
    __tablename__ = "alert_system"
    
    id = Column(Integer, primary_key=True, index=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    system = Column(String, nullable=False)
    alert_type = Column(SqlEnum(AlertType), nullable=False)
    message = Column(String, nullable=False)
    acknowledged = Column(Boolean, default=False, nullable=False)
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
    spacecraft = relationship("Spacecraft", back_populates="alerts")
