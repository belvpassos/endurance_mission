from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime


class NavigationStatus(str, Enum):
    OPERATIONAL = "operational"
    STANDBY = "standby"
    ERROR = "error"


class NavigationSystemBase(BaseModel):
    trajectory: str
    target_waypoint: str
    course_correction: Optional[int] = None
    delta_v_mps: Optional[float] = None
    burn_duration_seconds: Optional[float] = None
    alignment_error_deg: Optional[float] = None
    residual_drift_km: Optional[float] = None
    maneuver_window_open: Optional[datetime] = None
    maneuver_window_close: Optional[datetime] = None
    last_correction_at: Optional[datetime] = None
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
    target_waypoint: Optional[str] = None
    course_correction: Optional[int] = None
    delta_v_mps: Optional[float] = None
    burn_duration_seconds: Optional[float] = None
    alignment_error_deg: Optional[float] = None
    residual_drift_km: Optional[float] = None
    maneuver_window_open: Optional[datetime] = None
    maneuver_window_close: Optional[datetime] = None
    last_correction_at: Optional[datetime] = None
    navigation_system_status: Optional[NavigationStatus] = None
