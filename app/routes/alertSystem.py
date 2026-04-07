from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import alertSystem as models
from app.schemas import alertSystem as schemas
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/alerts", tags=["Alert System"])

@router.post("/", response_model=schemas.Alert, status_code=status.HTTP_201_CREATED)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    try:
        new_alert = models.AlertSystem(**alert.model_dump())
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        return new_alert
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create alert: {exc}")

@router.get("/{alert_id}", response_model=schemas.Alert)
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.AlertSystem).filter(models.AlertSystem.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.get("/", response_model=list[schemas.Alert])
def read_all_alerts(db: Session = Depends(get_db)):
    return db.query(models.AlertSystem).all()

@router.put("/{alert_id}", response_model=schemas.Alert)
def update_alert(alert_id: int, updated: schemas.AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(models.AlertSystem).filter(models.AlertSystem.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    try:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(alert, key, value)
        db.commit()
        db.refresh(alert)
        return alert
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update alert: {exc}")

@router.delete("/{alert_id}", response_model=OperationStatus)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.AlertSystem).filter(models.AlertSystem.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    try:
        db.delete(alert)
        db.commit()
        return OperationStatus(detail="Alert deleted successfully")
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete alert: {exc}")
