from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.abortRecoverySystem import AbortRecoverySystem
from app.schemas import abortRecoverySystem as schemas

router = APIRouter(prefix="/abort-recovery", tags=["Abort Recovery System"])


@router.post("/", response_model=schemas.AbortRecovery)
def create_abort_recovery(entry: schemas.AbortRecoveryCreate, db: Session = Depends(get_db)):
    new_entry = AbortRecoverySystem(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/{entry_id}", response_model=schemas.AbortRecovery)
def read_abort_recovery(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(AbortRecoverySystem).filter(AbortRecoverySystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Abort Recovery entry not found")
    return entry


@router.get("/", response_model=list[schemas.AbortRecovery])
def read_all_abort_recovery(db: Session = Depends(get_db)):
    return db.query(AbortRecoverySystem).all()


@router.put("/{entry_id}", response_model=schemas.AbortRecovery)
def update_abort_recovery(entry_id: int, updated: schemas.AbortRecoveryUpdate, db: Session = Depends(get_db)):
    entry = db.query(AbortRecoverySystem).filter(AbortRecoverySystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Abort recovery entry not found")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}")
def delete_abort_recovery(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(AbortRecoverySystem).filter(AbortRecoverySystem.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Abort Recovery entry not found")

    db.delete(entry)
    db.commit()
    return {"message": "Entry deleted successfully"}
