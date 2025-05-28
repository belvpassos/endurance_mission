from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import dockingSystem as schemas

router = APIRouter(prefix="/docking-system", tags=["Docking System"])

@router.post("/", response_model=schemas.DockingSystem)
def create_docking(entry: schemas.DockingSystemCreate, db: Session = Depends(get_db)):
    new_entry = models.DockingSystem(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/{entry_id}", response_model = schemas.DockingSystem)
def read_docking(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.DockingSystem).filter(models.DockingSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Docking entry not found")
    return entry

@router.get("/", response_model=list[schemas.DockingSystem])
def read_docking(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.DockSystem).filter(models.DockingSystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Docking entry not found")
    return entry

@router.get("/", response_model=list[schemas.DockingSystem])
def read_all_docking(db: Session = Depends(get_db)):
    return db.query(models.DockingSystem).all()

@router.put("/{entry_id}", response_model=schemas.DockingSystem)
def update_docking(entry_id: int, updated: schemas.DockingSystemUpdate, db: Session = Depends(get_db)):
   entry = db.query(models.DockingSystem).filter(models.DockingSystem.id == entry_id).first() 
   if entry is None:
       raise HTTPException(status_code=404, detail="Docking entry not found")
   
   for key, value in updated.dict(exclude_unset=True). items():
       setattr(entry, key, value)
       
       db.commit()
       db.refresh(entry)
       return entry
   
   @router.delete("/{entry_id}")
   def delete_docking(entry_id: int, db: Session = Depends(get_db)):
       entry = db.query(models.DockingSystem).filter(models.DOckingSystem.id == entry_id).first()
       if entry is None:
           raise HTTPException(status_code=404, detail="Docking entry not found")
       
       db.delete(entry)
       db.commit()
       return{"message":"Entry deleted successfully"}