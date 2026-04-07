from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.spacecraft import Spacecraft as SpacecraftModel
from app.schemas.spacecraft import Spacecraft, SpacecraftCreate, SpacecraftUpdate
from app.schemas.common import OperationStatus

router = APIRouter(prefix="/spacecraft", tags=["Spacecraft"])


@router.post("/", response_model=Spacecraft, status_code=status.HTTP_201_CREATED)
def create_spacecraft(spacecraft: SpacecraftCreate, db: Session = Depends(get_db)):
    db_spacecraft = SpacecraftModel(**spacecraft.model_dump())
    db.add(db_spacecraft)

    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not create spacecraft: {exc}")

    db.refresh(db_spacecraft)
    return db_spacecraft


@router.get("/", response_model=list[Spacecraft])
def read_spacecraft(db: Session = Depends(get_db)):
    return db.query(SpacecraftModel).all()


@router.get("/{spacecraft_id}", response_model=Spacecraft)
def read_spacecraft_by_id(spacecraft_id: int, db: Session = Depends(get_db)):
    spacecraft = db.query(SpacecraftModel).filter(SpacecraftModel.id == spacecraft_id).first()
    if not spacecraft:
        raise HTTPException(status_code=404, detail="Spacecraft not found")
    return spacecraft


@router.put("/{spacecraft_id}", response_model=Spacecraft)
def update_spacecraft(
    spacecraft_id: int, updated_spacecraft: SpacecraftUpdate, db: Session = Depends(get_db)
):
    spacecraft = db.query(SpacecraftModel).filter(SpacecraftModel.id == spacecraft_id).first()
    if not spacecraft:
        raise HTTPException(status_code=404, detail="Spacecraft not found")

    for key, value in updated_spacecraft.model_dump(exclude_unset=True).items():
        setattr(spacecraft, key, value)

    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not update spacecraft: {exc}")

    db.refresh(spacecraft)
    return spacecraft


@router.delete("/{spacecraft_id}", response_model=OperationStatus)
def delete_spacecraft(spacecraft_id: int, db: Session = Depends(get_db)):
    spacecraft = db.query(SpacecraftModel).filter(SpacecraftModel.id == spacecraft_id).first()
    if not spacecraft:
        raise HTTPException(status_code=404, detail="Spacecraft not found")

    try:
        db.delete(spacecraft)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not delete spacecraft: {exc}")

    return OperationStatus(detail="Spacecraft deleted successfully")
