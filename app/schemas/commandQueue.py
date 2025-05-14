from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class commandQueueBase(BaseModel):
    command: str
    parameters: Optional[str] = None
    schedule_time: Optional[datetime] = None
    executed: Optional [bool] = False
    executed_time: Optional[datetime] = None
    priority: Optional[int] = 1
    status: Optional[str] = "scheduled"
    spacecraft_id: int
    
    