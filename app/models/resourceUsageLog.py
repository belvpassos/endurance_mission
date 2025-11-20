from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, func
from app.database import Base


class ResourceUsageLog(Base):
    __tablename__ = "resource_usage_log"
    
    id = Column(Integer, primary_key=True, index=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    resource_type = Column(String, nullable=False)
    amount_used = Column(Float, nullable=False)
    amount_remaining = Column(Float, nullable=False)

    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
