from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.models.alertSystem import AlertSystem, AlertType
from app.models.missionEvents import EventType, MissionEvent
from app.models import navigationSystem as models
from app.schemas import navigationSystem as schemas
from app.schemas.common import OperationStatus
from app.services.missionState import sync_latest_mission_phase_from_event

router = APIRouter(prefix="/navigation-system", tags=["Navigation System"])

MONITORING_ALIGNMENT_THRESHOLD_DEG = 0.25
MONITORING_DRIFT_THRESHOLD_KM = 5.0
CRITICAL_ALIGNMENT_THRESHOLD_DEG = 1.0
CRITICAL_DRIFT_THRESHOLD_KM = 20.0
NAVIGATION_ALERT_SYSTEM = "Navigation Guidance"


def _create_course_correction_events(
    db: Session,
    entry: models.NavigationSystem,
    previous_course_correction: int,
) -> None:
    current_course_correction = entry.course_correction or 0
    if current_course_correction <= previous_course_correction:
        return

    for burn_number in range(previous_course_correction + 1, current_course_correction + 1):
        event = MissionEvent(
            event_type=EventType.COURSE_CORRECTION_BURN,
            timestamp=entry.last_correction_at or datetime.utcnow(),
            description=(
                f"Course correction burn {burn_number} executed toward {entry.target_waypoint} "
                f"with delta-v {entry.delta_v_mps or 0:.1f} m/s and residual drift "
                f"{entry.residual_drift_km or 0:.1f} km."
            ),
            spacecraft_id=entry.spacecraft_id,
        )
        db.add(event)
        sync_latest_mission_phase_from_event(db, event)


def _resolve_open_navigation_alert(alert: AlertSystem | None) -> None:
    if not alert:
        return
    alert.resolved = True
    alert.resolved_at = datetime.utcnow()


def _synchronize_navigation_alert(db: Session, entry: models.NavigationSystem) -> None:
    open_alert = (
        db.query(AlertSystem)
        .filter(
            AlertSystem.spacecraft_id == entry.spacecraft_id,
            AlertSystem.system == NAVIGATION_ALERT_SYSTEM,
            AlertSystem.resolved.is_(False),
        )
        .order_by(AlertSystem.timestamp.desc())
        .first()
    )

    alignment_error = entry.alignment_error_deg or 0.0
    residual_drift = entry.residual_drift_km or 0.0

    if alignment_error > CRITICAL_ALIGNMENT_THRESHOLD_DEG or residual_drift > CRITICAL_DRIFT_THRESHOLD_KM:
        alert_type = AlertType.CRITICAL
        message = (
            f"Navigation solution outside safety limits. Alignment error {alignment_error:.2f} deg, "
            f"residual drift {residual_drift:.1f} km. Immediate trajectory review required."
        )
    elif alignment_error > MONITORING_ALIGNMENT_THRESHOLD_DEG or residual_drift > MONITORING_DRIFT_THRESHOLD_KM:
        alert_type = AlertType.WARNING
        message = (
            f"Navigation drift elevated for waypoint {entry.target_waypoint}. Alignment error "
            f"{alignment_error:.2f} deg, residual drift {residual_drift:.1f} km."
        )
    else:
        _resolve_open_navigation_alert(open_alert)
        return

    if open_alert:
        open_alert.alert_type = alert_type
        open_alert.message = message
        open_alert.timestamp = datetime.utcnow()
        open_alert.resolved = False
        open_alert.resolved_at = None
        return

    db.add(
        AlertSystem(
            timestamp=datetime.utcnow(),
            system=NAVIGATION_ALERT_SYSTEM,
            alert_type=alert_type,
            message=message,
            acknowledged=False,
            resolved=False,
            spacecraft_id=entry.spacecraft_id,
        )
    )


@router.post("/", response_model=schemas.NavigationSystem, status_code=status.HTTP_201_CREATED)
def create_navigation(entry: schemas.NavigationSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.NavigationSystem(**entry.model_dump())
    try:
        db.add(new_entry)
        db.flush()
        _create_course_correction_events(db, new_entry, previous_course_correction=0)
        _synchronize_navigation_alert(db, new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create navigation entry: {exc}")


@router.get("/{entry_id}", response_model=schemas.NavigationSystem)
def read_navigation(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.NavigationSystem).filter(models.NavigationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Navigation entry not found")
    return entry


@router.get("/", response_model=list[schemas.NavigationSystem])
def read_all_navigation(db: Session = Depends(get_db)):
    return db.query(models.NavigationSystem).all()


@router.put("/{entry_id}", response_model=schemas.NavigationSystem)
def update_navigation(entry_id: int, updated: schemas.NavigationSystemUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.NavigationSystem).filter(models.NavigationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Navigation entry not found")

    previous_course_correction = entry.course_correction or 0
    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    try:
        _create_course_correction_events(db, entry, previous_course_correction=previous_course_correction)
        _synchronize_navigation_alert(db, entry)
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update navigation entry: {exc}")


@router.delete("/{entry_id}", response_model=OperationStatus)
def delete_navigation(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.NavigationSystem).filter(models.NavigationSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Navigation entry not found")

    try:
        db.delete(entry)
        db.commit()
        return OperationStatus(detail="Navigation entry deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete navigation entry: {exc}")
