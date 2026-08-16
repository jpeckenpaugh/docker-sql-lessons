from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    notes: Mapped[list["Note"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    lesson: Mapped["Lesson"] = relationship(back_populates="notes")
