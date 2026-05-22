from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class CommandStatus(str, Enum):
    QUEUED = "queued"
    EXECUTING = "executing"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    ABORTED = "aborted"

class CommandQueueBase(BaseModel):
    command: str
    parameters: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    executed: Optional[bool] = False
    executed_time: Optional[datetime] = None
    priority: Optional[int] = 1
    status: CommandStatus = CommandStatus.QUEUED
    spacecraft_id: int
    
class CommandQueueCreate(CommandQueueBase):
    pass

class CommandQueueUpdate(BaseModel):
    command: Optional[str] = None
    parameters: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    executed: Optional[bool] = None
    executed_time: Optional[datetime] = None
    priority: Optional[int] = None
    status: Optional[CommandStatus] = None
    spacecraft_id: Optional[int] = None

class CommandQueue(CommandQueueBase):
    id: int
    
    class Config:
        from_attributes = True
