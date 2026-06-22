from .base_entity import ( Column, String, Boolean, Enum, uuid4, enum, mapped_column, ForeignKey )
from ..database.config import Base
from sqlalchemy.orm import Mapped, relationship
from typing import List


class CoachEspecialidade(str, enum.Enum):
    musculacao = "musculacao"
    crossfit = "crossfit"
    yoga = "yoga"
    pilates = "pilates"
    natacao = "natacao"
    funcional = "funcional"


class CoachGenero(str, enum.Enum):
    masculino = "masculino"
    feminino = "feminino"
    outro = "outro"


class CoachEntity(Base):
    __tablename__ = "coaches"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    especialidade: Mapped[CoachEspecialidade] = mapped_column(Enum(CoachEspecialidade), nullable=False)
    genero: Mapped[CoachGenero] = mapped_column(Enum(CoachGenero), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=False)

    students: Mapped[List["StudentEntity"]] = relationship(
        "StudentEntity",
        back_populates="coach",
        cascade="all, delete-orphan"
    )
    experiencias: Mapped[List["CoachExperienciaEntity"]] = relationship(
        "CoachExperienciaEntity",
        cascade="all, delete-orphan",
        lazy="selectin"
    )