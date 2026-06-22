from ..database.config import Base
from .base_entity import String, uuid4, Mapped, mapped_column, ForeignKey
from sqlalchemy import Enum
import enum


class ExperienciaNome(str, enum.Enum):
    musculacao = "musculacao"
    crossfit = "crossfit"
    yoga = "yoga"
    pilates = "pilates"
    natacao = "natacao"
    funcional = "funcional"
    boxe = "boxe"
    artes_marciais = "artes_marciais"
    spinning = "spinning"
    zumba = "zumba"
    calistenia = "calistenia"
    alongamento = "alongamento"
    atletismo = "atletismo"
    nutricao_esportiva = "nutricao_esportiva"


class CoachExperienciaEntity(Base):
    __tablename__ = "coach_experiencias"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    coach_id: Mapped[str] = mapped_column(String(36), ForeignKey("coaches.id"), nullable=False)
    nome: Mapped[ExperienciaNome] = mapped_column(Enum(ExperienciaNome), nullable=False)