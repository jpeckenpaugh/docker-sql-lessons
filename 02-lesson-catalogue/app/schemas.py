from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LessonBase(BaseModel):
    title: str


class LessonCreate(LessonBase):
    pass


class Lesson(LessonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    notes: list["Note"] = []


class NoteBase(BaseModel):
    body: str


class NoteCreate(NoteBase):
    lesson_id: int


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int
    created_at: datetime


Lesson.model_rebuild()
