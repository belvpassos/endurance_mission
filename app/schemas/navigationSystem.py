from pydantic import BaseModel
from enum import Enum
from typing import Optional


class NavigationStatus(str, Enum):
    OPERATIONAL = "operational"
    STANDBY = "standby"
    ERROR = "error"


class NavigationSystemBase(BaseModel):
    trajectory: str
    course_correction: Optional[int] = None
    navigation_system_status: NavigationStatus


class NavigationSystemCreate(NavigationSystemBase):
    spacecraft_id: int


class NavigationSystem(NavigationSystemBase):
    id: int
    spacecraft_id: int

    class Config:
        from_attributes = True


class NavigationSystemUpdate(BaseModel):
    trajectory: Optional[str] = None
    course_correction: Optional[int] = None
    navigation_system_status: Optional[NavigationStatus] = None
