from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Session
from app.models.groundControlLog import GroundControlLog
from app.schemas.groundControlLog import GroundControlLogCreate, GrooundControlLogOut
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=GrooundControlLogOut)
def create_log(data: GroundControlLogCreate, db: Session = Depends(get_db)):
    log = GroundControlLog(**data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/", response_model=list[GrooundControlLogOut])
def read_all_logs(db: Session = Depends(get_d)):