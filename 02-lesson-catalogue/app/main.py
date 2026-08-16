from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/lessons", response_model=list[schemas.Lesson])
def list_lessons(db: Session = Depends(get_db)):
    return db.query(models.Lesson).all()


@app.post("/lessons", response_model=schemas.Lesson, status_code=201)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(get_db)):
    db_lesson = models.Lesson(**lesson.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@app.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson


@app.get("/notes", response_model=list[schemas.Note])
def list_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()


@app.post("/notes", response_model=schemas.Note, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    lesson = (
        db.query(models.Lesson).filter(models.Lesson.id == note.lesson_id).first()
    )
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db_note = models.Note(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
