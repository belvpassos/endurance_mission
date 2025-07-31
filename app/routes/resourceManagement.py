from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import Session
from app.database import get_db
from app.models import resourceManagement as models
from app.schemas import resourceManagement as schemas

router = APIRouter(prefix="/resource-management", tags=["Resource Management"])

@router.post("/", response_model=schemas.ResourceManagement)
def create_resource(entry: schemas.ResourceManagementCreate, db: Session = Depends(get_db)):
    new_entry = models.ResourceManagement(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return (new_entry)

@router.get("/{entry_id}", response_model=schemas.ResourceManagement)
def read_resource(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.ResourceManagement).filter(models.ResourceManagement.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.get("/", response_model=list[schemas.ResourceManagement])
def read_all_resource(db: Session = Depends(get_db)):
    return db.query(models.ResourceManagement).all()

@router.put("/{entry_id}", response_model=schemas.ResourceManagement)
def update_resource(entry_id: int, updated: schemas.ResourceManagementUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.ResourceManagement).filter(models.ResourceManagement.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry

@router.delete("/{entry_id}")
def delete_resource(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.ResourceManagement).filter(models.ResourceManagement.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    db.delete(entry)
    db.commit()
    return {"message":"Resource entry deleted successfully!"}