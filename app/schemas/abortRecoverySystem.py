from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# Enum compatível com o model
class AbortStatusEnum(str, Enum):
    standby = "standby"
    triggered = "triggered"
    recovered = "recovered"

# Base schema
class AbortRecoveryBase(BaseModel):
    status: Optional[AbortStatusEnum] = AbortStatusEnum.standby
    abort_reason: Optional[str] = None
    triggered_at: Optional[datetime] = None
    recovery_procedure: Optional[str] = None
    success: Optional[bool] = False
    spacecraft_id: int

# Schema para criação
class AbortRecoveryCreate(AbortRecoveryBase):
    pass

# Schema para atualização
class AbortRecoveryUpdate(BaseModel):
    status: Optional[AbortStatusEnum]
    abort_reason: Optional[str]
    triggered_at: Optional[datetime]
    recovery_procedure: Optional[str]
    success: Optional[bool]

# Schema de resposta
class AbortRecovery(AbortRecoveryBase):
    id: int

    class Config:
        from_attributes = True
