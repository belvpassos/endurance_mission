from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class SubsystemDiagnostics (Base):
    __tablename__ = "subsystem_diagnostics"
    
    id = Column(Integer, primary_key=True, index=True)
    subsystem_name = Column(String, nullable=False)
    diagnostic_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default = "Nominal")
    report = Column(Text)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))