from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.spacecraftStatus import SpacecraftStatus as SpacecraftStatusModel
from app.schemas.spacecraftStatus import SpacecraftStatusCreate, SpacecraftStatusResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/spacecraft_status/", response_model=SpacecraftStatusResponse)
def create_spacecraft_status(status: SpacecraftStatusCreate, db: Session = Depends(get_db)):
    db_status = SpacecraftStatusModel(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

@router.get("/spacecraft_status/", response_model=list[SpacecraftStatusResponse])
def read_spacecraft_status(db: Session = Depends(get_db)):
    return db.query(SpacecraftStatusModel).all()

@router.get("/spacecraft_status/{status_id}", response_model=SpacecraftStatusResponse)
def read_spacecraft_status_by_id(status_id: int, db: Session = Depends(get_db)):
    status = db.query(SpacecraftStatusModel).filter(SpacecraftStatusModel.id == status_id).first()
    if status is None:
        raise HTTPException(status_code=404, detail="Status can't be found")
    return status

@router.put("/spacecraft_status/{status_id}", response_model=SpacecraftStatusResponse)
def update_spacecraft_status(status_id: int, updated_status: SpacecraftStatusCreate, db: Session = Depends(get_db)):
    status = db.query(SpacecraftStatusModel).filter(SpacecraftStatusModel.id == status_id).first()
    if status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    
    for key, value in updated_status.dict(exclude_unset=True).items():
        setattr(status, key, value)

    db.commit()
    db.refresh(status)
    return status

@router.delete("/spacecraft_status/{status_id}")
def delete_spacecraft_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(SpacecraftStatusModel).filter(SpacecraftStatusModel.id == status_id).first()
    if status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    
    db.delete(status)
    db.commit()
    return{"detail": "Spacecraft status deleted successfully"}
    