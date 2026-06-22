from .base_entity import String, Boolean, Enum, uuid4, enum, mapped_column, ForeignKey
from ..database.config import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import DateTime
from datetime import datetime
from typing import Optional, List


class StudentGenero(str, enum.Enum):
    masculino = "masculino"
    feminino = "feminino"
    outro = "outro"


class StudentEntity(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    genero: Mapped[StudentGenero] = mapped_column(Enum(StudentGenero), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=False)

    data_inicio: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    data_fim: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    coach_id: Mapped[str] = mapped_column(String, ForeignKey("coaches.id"), nullable=False)
    payment_plan_id: Mapped[str] = mapped_column(String, ForeignKey("planos_pagamento.id"), nullable=False)

    coach: Mapped["CoachEntity"] = relationship("CoachEntity", back_populates="students")
    payment_plan: Mapped["PaymentPlanEntity"] = relationship("PaymentPlanEntity", back_populates="students")

    pagamentos: Mapped[List["PaymentEntity"]] = relationship(
        "PaymentEntity",
        back_populates="student",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    attendances: Mapped[List["AttendanceEntity"]] = relationship(
        "AttendanceEntity",
        back_populates="student",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    @property
    def dias_restantes(self) -> int:
        if self.data_fim is None:
            return 0
        hoje = datetime.utcnow()
        if hoje >= self.data_fim:
            return 0
        return (self.data_fim - hoje).days