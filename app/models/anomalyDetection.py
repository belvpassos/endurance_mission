import enum
from sqlalchemy import Column, Integer, Text, Enum as SqlEnum, ForeignKey
from app.database import Base

class PriorityLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
class AnomalyDetection(Base):
    __tablename__ = "anomaly_detection"
    
    id = Column(Integer, primary_key=True, index=True)
    anomaly_logs = Column(Text, nullable=False)   # logs podem ser longos
    system_alerts = Column(Text, nullable=False)  # mensagens do sistema também
    priority_level = Column(
        SqlEnum(PriorityLevel, values_callable=lambda enum_cls: [item.value for item in enum_cls], native_enum=False),
        nullable=False,
    )
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
