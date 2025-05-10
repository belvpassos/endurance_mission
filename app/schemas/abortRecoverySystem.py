from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AbortRecoveryBase(BaseModel):
    status: Optional[str] = "standby"
    abort_reason: Optional[str] = None
    triggered_at:  Optional[datetime] = None
    recovery_procedure: Optional[str] = None
    success: Optional[bool] = False
    spacecraft_id: int
    
class AbortRecoveryCreate(AbortRecoveryBase):
    pass

class AbortRecoveryUpdate(BaseModel):
    status: Optional[str]
    abort_reason: Optional[str]
    triggered_at: Optional[datetime]
    recovery_procedure: Optional[str]
    success: Optional[bool]
    
class AbortRecovery(AbortRecoveryBase):
    id: int
    
class config:
    orm_mode: True