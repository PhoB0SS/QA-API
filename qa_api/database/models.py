"""ORM database templates for SQLAlchemy"""

from typing import List
from datetime import datetime

from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    """Base model"""

    pass

class Question(Base):
    """Question model"""

    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    answers: Mapped[List["Answer"]] = relationship(back_populates='question', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, text='{self.text[:20]}', created_at={self.created_at})>"

class Answer(Base):
    """Answer model"""

    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    question: Mapped["Question"] = relationship(back_populates="answers")

    def __repr__(self) -> str:
        return (f"<Answer(id={self.id}, question_id={self.question_id}, "
                f"user_id='{self.user_id}', text='{self.text[:20]}', created_at={self.created_at})>")
