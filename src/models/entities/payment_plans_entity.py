from ..database.config import Base
from .base_entity import (
    String, Float, Integer, uuid4,
    Mapped, mapped_column, Boolean, relationship, List
)
from .payment_plan_exercise_entity import PaymentPlanExerciseEntity


class PaymentPlanEntity(Base):
    __tablename__ = "planos_pagamento"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))

    nome: Mapped[str] = mapped_column(String(100), unique=True)
    preco: Mapped[float] = mapped_column(Float)
    duracao_dias: Mapped[int] = mapped_column(Integer)

    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    exercicios: Mapped[List["PaymentPlanExerciseEntity"]] = relationship(
        "PaymentPlanExerciseEntity",   # ✅ nome exacto da classe
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    students: Mapped[List["StudentEntity"]] = relationship(
        "StudentEntity",
        back_populates="payment_plan",
        lazy="selectin"
    )