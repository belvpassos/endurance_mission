import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.database import Base

class PriorityLevel(enum, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
class AnomalyDetection(Base):
    __tablename__ = "anomaly_detection"
    
    id = Column(Integer, primary_key=True, index=True)
    anomaly_logs = Column(String)
    system_alerts = Column(String)
    priority_level = Column(Enum(PriorityLevel), nullable=False)
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"))