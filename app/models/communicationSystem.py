import enum
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from app.database import Base

class LinkStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class CommunicationSystem(Base):
    __tablename__ = "communication_system"
    
    id = Column(Integer, primary_key=True, index=True)
    latency = Column(Float)
    signal_strength = Column(Float)
    uplink_status = Column(Enum(LinkStatus), nullable=False)
    downlink_status = Column(Enum(LinkStatus), nullable=False)
    last_contact_time = Column(DateTime)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))