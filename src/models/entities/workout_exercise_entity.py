from ..database.config import Base
from .base_entity import String, Integer, Float, uuid4, Mapped, mapped_column, ForeignKey
from sqlalchemy import Enum
import enum


class DiaSemana(str, enum.Enum):
    segunda = "segunda"
    terca = "terca"
    quarta = "quarta"
    quinta = "quinta"
    sexta = "sexta"
    sabado = "sabado"
    domingo = "domingo"


class WorkoutExerciseEntity(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))

    workout_plan_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("workout_plans.id", ondelete="CASCADE")
    )

    dia_semana: Mapped[DiaSemana] = mapped_column(Enum(DiaSemana), nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    series: Mapped[int] = mapped_column(Integer, nullable=False)
    repeticoes: Mapped[int] = mapped_column(Integer, nullable=False)
    carga: Mapped[float] = mapped_column(Float, nullable=True)  # kg, opcional