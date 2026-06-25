from ..database.config import Base
from .base_entity import (
    String, Boolean, uuid4,
    Mapped, mapped_column, relationship, List, ForeignKey
)
from sqlalchemy import DateTime
from datetime import datetime


class WorkoutPlanEntity(Base):
    __tablename__ = "workout_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))

    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"), nullable=False)
    coach_id: Mapped[str] = mapped_column(String(36), ForeignKey("coaches.id"), nullable=False)

    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    exercicios: Mapped[List["WorkoutExerciseEntity"]] = relationship(
        "WorkoutExerciseEntity",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    student: Mapped["StudentEntity"] = relationship("StudentEntity")
    coach: Mapped["CoachEntity"] = relationship("CoachEntity")