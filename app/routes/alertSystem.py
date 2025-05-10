from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import alertSystem as schemas

router = APIRouter(prefix="/alerts", tags=["Alert System"])

@router.post("/", response_model=schemas.Alert)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    new_alert = models.alertSystem.AlertSystem(**alert.dict())
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

@router.get("/{alert_id}", response_model=schemas.Alert)
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.alertSystem.AlertSystem).filter(models.alertSystem.AlertSystem.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.get("/", response_model=list[schemas.Alert])
def read_all_alerts(db: Session = Depends(get_db)):
    return db.query(models.alertSystem.AlertSystem).all()

@router.put("/{alert_id}", response_model=schemas.Alert)
def update_alert(alert_id: int, updated: schemas.AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(models.alertSystem.AlertSystem).filter(models.alertSystem.AlertSystem.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(alert, key, value)
    
    db.commit()
    db.refresh(alert)
    return alert


@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.alertSystem.AlertSystem).filter(models.alertSystem.AlertSystem.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted successfully"}