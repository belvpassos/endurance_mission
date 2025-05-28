from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DataRecorderBase(BaseModel):
    timestamp: Optional[datetime] = None
    date_type: str
    data_value: str
    source_system: str

class DataRecorderCreate(DataRecorderBase):
    spacecraft_id: int

class DataRecorderUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    date_type: Optional[str] = None
    data_value: Optional[str] = None
    source_system: Optional[str] = None
    spacecraft_id: Optional[int] = None

class DataRecorder(DataRecorderBase):
    id: int
    spacecraft_id: int

    class Config:
        orm_mode = True
