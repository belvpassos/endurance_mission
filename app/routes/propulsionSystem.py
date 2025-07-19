from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import propulsionSystem as schemas

router = APIRouter(prefix="/propulsion-system", tags=["Propulsion System"])

@router.post("/", response_model=schemas.PropulsionSystem)
def create_propulsion(entry: schemas.PropulsionSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.PropulsionSystem(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return 

@router.get("/", response_model=schemas.PropulsionSystem)
def read_propulsion(entry_id: int, db: Session = Depends(get_db)):
    entry = db.entry(models.PropulsionSystem).filter(models.PropulsionSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail= "Entry not found")
    return entry


@router.get("/", response_model=list[schemas.PropulsionSystem])
def read_all_propulsion(db:Session = Depends(get_db)):
    return db.query(models.PropulsionSystem).all()

@router.put("/{entry_id}", response_model=schemas.PropulsionSystem)
def update_propulsion(entry_id: int, updated: schemas.PropulsionSystem, db: Session = Depends(get_db)):
    entry = db.query(models.PropulsionSystem).filter(models.PropulsionSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    for key, value in updated.dict(exclude_unset = True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}")
def delete_power(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.PropulsionSystem).filter(models.PropulsionSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    db.delete(entry)
    db.commit()
    return{"message":"Entry deleted successfully"}