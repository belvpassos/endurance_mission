from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import alertSystem as models
from app.schemas import alertSystem as schemas

router = APIRouter(prefix="/alerts", tags=["Alert System"])

@router.post("/", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    try:
        new_alert = models.AlertSystem(**alert.dict())
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        return new_alert
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating alert: {e}")

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
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(alert, key, value)
        db.commit()
        db.refresh(alert)
        return alert
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating alert: {e}")

@router.delete("/{alert_id}", response_model=dict)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.AlertSystem).filter(models.AlertSystem.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    try:
        db.delete(alert)
        db.commit()
        return {"message": "Alert deleted successfully", "id": alert_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting alert: {e}")
