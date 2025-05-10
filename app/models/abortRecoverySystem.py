from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class AbortRecoverySystem(Base):
    __tablename__ = "abort_recovery_system"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="standby")
    abort_reason = Column(String, nullable=True)
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    recovery_procedure = Column(String, nullable=True)
    success = Column(Boolean, default=False)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))