import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, DateTime
from datetime import datetime
from app.database import Base


class NavigationStatus(enum.Enum):
    OPERATIONAL = "operational"
    STANDBY = "standby"
    ERROR = "error"


class NavigationSystem(Base):
    __tablename__ = "navigation_system"

    id = Column(Integer, primary_key=True, index=True)
    trajectory = Column(String, nullable=False)
    target_waypoint = Column(String, nullable=False)
    course_correction = Column(Integer, nullable=True, default=0)
    delta_v_mps = Column(Float, nullable=True)
    burn_duration_seconds = Column(Float, nullable=True)
    alignment_error_deg = Column(Float, nullable=True)
    residual_drift_km = Column(Float, nullable=True)
    maneuver_window_open = Column(DateTime, nullable=True)
    maneuver_window_close = Column(DateTime, nullable=True)
    last_correction_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    navigation_system_status = Column(
        Enum(NavigationStatus, values_callable=lambda enum_cls: [item.value for item in enum_cls], native_enum=False),
        nullable=False,
    )

    spacecraft_id = Column(Integer, ForeignKey("spacecraft.id"), nullable=False)
