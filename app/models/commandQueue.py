from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database import Base
from datetime import datetime

class CommandQueue(Base):
    __tablename__ = "command_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    
    command = Column(String, nullable=False)
    parameters = Column(String)
    scheduled_time = Column(DateTime)
    executed = Column(Boolean, default=False)
    executed_time = Column(DateTime, nullable=True)
    priority = Column(Integer, default=1)
    status = Column(String, default="scheduled")
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))