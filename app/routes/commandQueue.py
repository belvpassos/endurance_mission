from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import commandQueue as schemas

router = APIRouter(prefix="/command-queue", tags=["Command Queue"])

@router.post("/", response_model=schemas.CommandQueue)
def create_command(entry: schemas.CommandQueueCreate, db: Session = Depends(get_db)):
    new_entry = models.CommandQueue(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.get("/{entry_id}", response_model=schemas.CommandQueue)
def read_command(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommandQueue).filter(models.CommandQueue.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Command not found")
    return entry

@router.get("/", response_model=list[schemas.CommandQueue])
def read_all_commands(db: Session = Depends(get_db)):
    return db.query(models.CommandQueue).all()

@router.put("/{entry_id}", response_model=schemas.CommandQueue)
def uodate_command(entry_id: int, updated: schemas.CommandQueueUpdate, db: Session = Depends(get_db)):
    entry = db.query (models.CommandQueue).filter(models.CommandQueue.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail= "Command not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)
        
    db.commit()
    db.refresh(entry)
    return entry                 

@router.delete("/{entry_id}")
def delete_command(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.CommandQueue).filter(models.CommandQueue.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Command not found")
    
    db.delete(entry)
    db.commit()
    return {"message": "Commanc deleted successfully"}
    