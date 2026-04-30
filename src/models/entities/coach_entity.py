from .base_entity import ( Column, String, Boolean, Enum, uuid4, enum, mapped_column, relationship )
from ..database.config import Base
from sqlalchemy.orm import Mapped, relationship


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
    ativo: Mapped[bool] = mapped_column(Boolean, default=False)  # False até o admin activar

    students: Mapped[list["StudentEntity"]] = relationship("StudentEntity", back_populates="coach")