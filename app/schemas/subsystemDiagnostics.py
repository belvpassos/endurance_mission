from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubsystemDiagnosticsBase(BaseModel):
    subsystem_name: str
    diagnostic_time: Optional[datetime] = None
    status: Optional[str] = "Nominal"
    report: Optional[str] = None
    spacecraft_id: int

class SubsystemDiagnosticsCreate(SubsystemDiagnosticsBase):
    pass

class SubsystemDiagnosticsUpdate(BaseModel):
    subsystem_name: Optional[str] = None
    diagnostic_time: Optional[datetime] = None
    status: Optional[str] = None
    report: Optional[str] = None

class SubsystemDiagnosticsResponse(SubsystemDiagnosticsBase):
    id: int

    class Config:
        orm_mode = True
