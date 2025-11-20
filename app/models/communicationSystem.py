import enum
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum as SqlEnum
from app.database import Base

class LinkStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class CommunicationSystem(Base):
    __tablename__ = "communication_system"
    
    id = Column(Integer, primary_key=True, index=True)
    latency = Column(Float, nullable=True)
    signal_strength = Column(Float, nullable=True)
    uplink_status = Column(SqlEnum(LinkStatus), nullable=False)
    downlink_status = Column(SqlEnum(LinkStatus), nullable=False)
    last_contact_time = Column(DateTime, nullable=True)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
