import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum as SqlEnum

from app.database import Base


class CommandStatus(enum.Enum):
    QUEUED = "queued"
    EXECUTING = "executing"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    ABORTED = "aborted"

class CommandQueue(Base):
    __tablename__ = "command_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    command = Column(String, nullable=False)
    parameters = Column(String, nullable=True)
    scheduled_time = Column(DateTime, default=datetime.utcnow)
    executed = Column(Boolean, default=False)
    executed_time = Column(DateTime, nullable=True)
    priority = Column(Integer, default=1)
    status = Column(
        SqlEnum(CommandStatus, values_callable=lambda enum_cls: [item.value for item in enum_cls], native_enum=False),
        default=CommandStatus.QUEUED.value,
        nullable=False,
    )
    
    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
