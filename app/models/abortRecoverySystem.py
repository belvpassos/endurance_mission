from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

# Enum opcional para limitar status
class AbortStatusEnum(str, enum.Enum):
    standby = "standby"
    triggered = "triggered"
    recovered = "recovered"

class AbortRecoverySystem(Base):
    __tablename__ = "abort_recovery_system"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Status limitado a valores definidos
    status = Column(Enum(AbortStatusEnum), default=AbortStatusEnum.standby, nullable=False)
    
    abort_reason = Column(String, nullable=True)
    
    # Sempre ter um timestamp inicial
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    recovery_procedure = Column(String, nullable=True)
    
    success = Column(Boolean, default=False, nullable=False)
    
    # Relacionamento com spacecraft
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
    spacecraft = relationship("Spacecraft", back_populates="abort_systems")  # se Spacecraft tiver abort_systems
