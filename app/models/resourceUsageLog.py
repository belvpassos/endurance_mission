from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from app.database import Base
from datetime import datetime

class ResourceUsageLog(Base):
    __tablename__ = "resource_usage_log"
    
    id = Column(Integer, primary_key= True, index=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    resource_type = Column(String)
    amount_used = Column(Float)
    amount_remaining = Column(Float)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))
    