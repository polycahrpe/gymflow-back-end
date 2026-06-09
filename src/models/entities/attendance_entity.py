from ..database.config import Base
from .base_entity import (
    String, uuid4,
    Mapped, mapped_column, relationship
)
from sqlalchemy import Date, Time, DateTime, Enum, ForeignKey
import enum
from datetime import date, time, datetime


class AttendanceStatus(str, enum.Enum):
    pendente_entrada = "pendente_entrada"
    presente         = "presente"
    pendente_saida   = "pendente_saida"
    saiu             = "saiu"


class AttendanceEntity(Base):
    __tablename__ = "attendances"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    hora_entrada: Mapped[time | None] = mapped_column(Time, nullable=True)
    hora_saida: Mapped[time | None] = mapped_column(Time, nullable=True)
    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus),
        default=AttendanceStatus.pendente_entrada,
        nullable=False
    )
    confirmado_entrada_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    confirmado_saida_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    student: Mapped["StudentEntity"] = relationship("StudentEntity", lazy="selectin")