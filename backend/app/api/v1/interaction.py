from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.models.interaction import Interaction
from backend.app.schemas.interaction import InteractionCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/log")
def log_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    obj = Interaction(
        hcp_name=data.hcp_name,
        notes=data.notes
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(Interaction).all()