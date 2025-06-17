from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class DataRecorder(Base):
    __tablename__ = "data_recorder"
    
    id = Column(Integer, primary_key=True, index=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    date_type = Column(String)
    data_value = Column(String)
    source_system = Column(String)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))