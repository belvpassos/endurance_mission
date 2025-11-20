from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class DataRecorder(Base):
    __tablename__ = "data_recorder"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_type = Column(String, nullable=False)  
    data_value = Column(String, nullable=False)  
    source_system = Column(String, nullable=False)    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)

    spacecraft = relationship("Spacecraft", back_populates="data_records")
