from ..database.config import Base
from .base_entity import (
    String, Float, uuid4,
    Mapped, mapped_column, relationship, List
)
from sqlalchemy import Date, Enum, ForeignKey
import enum
from datetime import date


class PaymentStatus(str, enum.Enum):
    pago = "pago"
    pendente = "pendente"
    atrasado = "atrasado"


class PaymentEntity(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))

    student_id: Mapped[str] = mapped_column(String(36), ForeignKey("students.id"), nullable=False)
    payment_plan_id: Mapped[str] = mapped_column(String(36), ForeignKey("planos_pagamento.id"), nullable=False)

    valor: Mapped[float] = mapped_column(Float, nullable=False)
    data_pagamento: Mapped[date] = mapped_column(Date, nullable=False)
    data_vencimento: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.pendente)
    observacao: Mapped[str | None] = mapped_column(String(255), nullable=True)

    student: Mapped["StudentEntity"] = relationship("StudentEntity")
    payment_plan: Mapped["PaymentPlanEntity"] = relationship("PaymentPlanEntity")