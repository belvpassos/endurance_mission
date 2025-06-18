from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Session
from app.models.groundControlLog import GroundControlLog
from app.schemas.groundControlLog import GroundControlLogCreate, GroundControlLogOut
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=GroundControlLogOut)
def create_log(data: GroundControlLogCreate, db: Session = Depends(get_db)):
    log = GroundControlLog(**data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/", response_model=list[GroundControlLogOut])
def read_all_logs(db: Session = Depends(get_db)):
    return db.query(GroundControlLog).all()

@router.get("/{id}", response_model=GroundControlLogOut)
def read_log(id: int, db: Session = Depends(get_db)):
    log = db.query(GroundControlLog).filter(GroundControlLog.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
    
@router.put("/{id}", response_model=GroundControlLogOut)
def update_log(id: int, data: GroundControlLogCreate, db: Session = Depends(get_db)):
    log = db.query(GroundControlLog).filter(GroundControlLog.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    for key, value in data.dict().items():
        setattr(log, key, value)
        db.commit()
        db.refresh(log)
        return log
    
    @router.delete("/{id}")
    def delete_log(id: int, Session = Depends(get_db)):
        log = db.query(GroundControlLog).filter(GroundControlLog.id == id).first()
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        db.delete(log)
        db.commit()
        return{"detail":"Log deleted"}