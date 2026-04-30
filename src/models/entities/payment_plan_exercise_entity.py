from ..database.config import Base
from .base_entity import ( String, uuid4, Mapped, mapped_column, ForeignKey )

class PaymentPlanExerciseEntity(Base):
    __tablename__ = "plano_exercicios"
 
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
 
    plano_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("planos_pagamento.id", ondelete="CASCADE")
    )
 
    nome: Mapped[str] = mapped_column(String(100))