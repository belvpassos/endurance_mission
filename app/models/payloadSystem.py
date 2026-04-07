import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from app.database import Base
from datetime import datetime


class PayloadStatus(enum.Enum):
    ACTIVE = "active"
    STANDBY = "standby"
    DEPLOYED = "deployed"
    FAILED = "failed"
    DECOMMISSIONED = "decommissioned"


class PayloadSystem(Base):
    __tablename__ = "payload_system"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(
        Enum(PayloadStatus, values_callable=lambda enum_cls: [item.value for item in enum_cls], native_enum=False),
        nullable=False,
        default=PayloadStatus.STANDBY,
    )
    mass = Column(Float, nullable=True)
    power_requirement = Column(Float, nullable=True)
    data_rate = Column(Float, nullable=True)
    deployment_time = Column(DateTime, default=datetime.utcnow)

    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
