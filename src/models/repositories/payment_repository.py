from .base_repository import HTTPException, status, Session
from datetime import timedelta, datetime
from sqlalchemy.orm import joinedload
from ..entities.payment_entity import PaymentEntity, PaymentStatus
from ..entities.student_entity import StudentEntity
from ..entities.payment_plans_entity import PaymentPlanEntity
from ...schemas.payment_schema import PaymentCreateSchema, PaymentUpdateSchema


class PaymentRepository:
    def __init__(self, my_session: Session):
        self.session = my_session

    # ─────────────────────────────────────────
    # GET ALL
    # ─────────────────────────────────────────
    def get_all(self):
        return (
            self.session.query(PaymentEntity)
            .options(
                joinedload(PaymentEntity.student),
                joinedload(PaymentEntity.payment_plan)
            )
            .all()
        )

    # ─────────────────────────────────────────
    # GET BY STUDENT
    # ─────────────────────────────────────────
    def get_by_student(self, student_id: str):
        return (
            self.session.query(PaymentEntity)
            .options(
                joinedload(PaymentEntity.student),
                joinedload(PaymentEntity.payment_plan)
            )
            .filter(PaymentEntity.student_id == student_id)
            .all()
        )

    # ─────────────────────────────────────────
    # GET BY ID
    # ─────────────────────────────────────────
    def get_by_id(self, id: str):
        payment = (
            self.session.query(PaymentEntity)
            .options(
                joinedload(PaymentEntity.student),
                joinedload(PaymentEntity.payment_plan)
            )
            .filter(PaymentEntity.id == id)
            .first()
        )
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
        student = self.session.query(StudentEntity).filter(
            StudentEntity.id == data.student_id
        ).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )

        plano = self.session.query(PaymentPlanEntity).filter(
            PaymentPlanEntity.id == data.payment_plan_id
        ).first()
        if not plano:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de pagamento não encontrado."
            )

        if data.valor != plano.preco:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O valor pago ({data.valor}) não corresponde ao preço do plano ({plano.preco})."
            )

        # Verifica sobreposição
        ultimo_pagamento = (
            self.session.query(PaymentEntity)
            .filter(PaymentEntity.student_id == data.student_id)
            .order_by(PaymentEntity.data_vencimento.desc())
            .first()
        )

        if ultimo_pagamento and data.data_pagamento <= ultimo_pagamento.data_vencimento:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Este pagamento sobrepõe-se ao anterior. "
                       f"O próximo pagamento deve começar após {ultimo_pagamento.data_vencimento}."
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

        hoje = datetime.utcnow().date()

        if student.data_fim is None or student.data_fim.date() <= hoje:
            student.data_inicio = datetime.combine(data.data_pagamento, datetime.min.time())
            student.data_fim = datetime.combine(data_vencimento, datetime.min.time())
        else:
            nova_data_fim = student.data_fim.date() + timedelta(days=plano.duracao_dias)
            student.data_fim = datetime.combine(nova_data_fim, datetime.min.time())

        student.payment_plan_id = data.payment_plan_id
        student.ativo = True

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
        student_id = payment.student_id

        self.session.delete(payment)
        self.session.flush()

        hoje = datetime.utcnow().date()

        # Pagamentos válidos restantes
        pagamentos_validos = (
            self.session.query(PaymentEntity)
            .filter(
                PaymentEntity.student_id == student_id,
                PaymentEntity.data_vencimento >= hoje
            )
            .order_by(PaymentEntity.data_vencimento.desc())
            .all()
        )

        # Todos os pagamentos restantes para determinar data_inicio
        pagamentos_restantes = (
            self.session.query(PaymentEntity)
            .filter(PaymentEntity.student_id == student_id)
            .order_by(PaymentEntity.data_pagamento.asc())
            .all()
        )

        student = self.session.query(StudentEntity).filter(
            StudentEntity.id == student_id
        ).first()

        if pagamentos_validos:
            ultimo_valido = pagamentos_validos[0]
            primeiro = pagamentos_restantes[0]
            student.data_inicio = datetime.combine(primeiro.data_pagamento, datetime.min.time())
            student.data_fim = datetime.combine(ultimo_valido.data_vencimento, datetime.min.time())
            student.ativo = True
        else:
            student.data_inicio = None
            student.data_fim = None
            student.ativo = False

        self.session.commit()
        return {"detail": "Pagamento eliminado com sucesso."}