from .base_repository import HTTPException, status, Session
from datetime import timedelta
from ..entities.payment_entity import PaymentEntity, PaymentStatus
from ..entities.payment_plans_entity import PaymentPlanEntity
from ...schemas.payment_schema import PaymentCreateSchema, PaymentUpdateSchema


class PaymentRepository:
    def __init__(self, my_session: Session):
        self.session = my_session

    # ─────────────────────────────────────────
    # GET ALL
    # ─────────────────────────────────────────
    def get_all(self):
        return self.session.query(PaymentEntity).all()

    # ─────────────────────────────────────────
    # GET ALL BY STUDENT
    # ─────────────────────────────────────────
    def get_by_student(self, student_id: str):
        return self.session.query(PaymentEntity).filter(
            PaymentEntity.student_id == student_id
        ).all()

    # ─────────────────────────────────────────
    # GET BY ID
    # ─────────────────────────────────────────
    def get_by_id(self, id: str):
        payment = self.session.query(PaymentEntity).filter(
            PaymentEntity.id == id
        ).first()

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pagamento não encontrado."
            )

        return payment

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────
    def create(self, data: PaymentCreateSchema):
        # Busca o plano para calcular a data de vencimento
        plano = self.session.query(PaymentPlanEntity).filter(
            PaymentPlanEntity.id == data.payment_plan_id
        ).first()

        if not plano:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de pagamento não encontrado."
            )

        data_vencimento = data.data_pagamento + timedelta(days=plano.duracao_dias)

        payment = PaymentEntity(
            student_id=data.student_id,
            payment_plan_id=data.payment_plan_id,
            valor=data.valor,
            data_pagamento=data.data_pagamento,
            data_vencimento=data_vencimento,
            status=PaymentStatus.pago,
            observacao=data.observacao,
        )

        self.session.add(payment)
        self.session.commit()
        self.session.refresh(payment)

        return payment

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────
    def update(self, id: str, data: PaymentUpdateSchema):
        payment = self.get_by_id(id)

        if data.valor is not None:
            payment.valor = data.valor
        if data.data_pagamento is not None:
            payment.data_pagamento = data.data_pagamento
        if data.status is not None:
            payment.status = data.status
        if data.observacao is not None:
            payment.observacao = data.observacao

        self.session.commit()
        self.session.refresh(payment)

        return payment

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────
    def delete(self, id: str):
        payment = self.get_by_id(id)

        self.session.delete(payment)
        self.session.commit()

        return {"detail": "Pagamento eliminado com sucesso."}