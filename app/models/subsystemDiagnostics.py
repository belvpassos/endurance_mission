from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SubsystemDiagnostics(Base):
    __tablename__ = "subsystem_diagnostics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    subsystem_name = Column(String, nullable=False, index=True)
    diagnostic_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, default="Nominal", nullable=False)
    report = Column(Text, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)

    # opcional — só se você quiser a relação no modelo spacecraft
    # spacecraft = relationship("Spacecraft", back_populates="diagnostics")
