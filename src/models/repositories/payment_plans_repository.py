from .base_repository import ( HTTPException, status, Session )

from ..entities.payment_plans_entity import PaymentPlanEntity
from ..entities.payment_plan_exercise_entity import PaymentPlanExerciseEntity
from ...schemas.payment_plans_schema import PaymentPlansCreateSchema, PaymentPlansUpdateSchema


class PaymentPlansRepository:
    def __init__(self, my_session: Session):
        self.session = my_session

    # ─────────────────────────────────────────
    # GET ALL
    # ─────────────────────────────────────────
    def get_all(self):
        return self.session.query(PaymentPlanEntity).all()

    # ─────────────────────────────────────────
    # GET BY ID
    # ─────────────────────────────────────────
    def get_by_id(self, id: str):
        plano = self.session.query(PaymentPlanEntity).filter(
            PaymentPlanEntity.id == id
        ).first()

        if not plano:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de pagamento não encontrado."
            )

        return plano

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────
    def create(self, data: PaymentPlansCreateSchema):
        plano = PaymentPlanEntity(
            nome=data.nome,
            preco=data.preco,
            duracao_dias=data.duracao_dias,
        )

        # Converte lista de strings em entidades
        plano.exercicios = [
            PaymentPlanExerciseEntity(nome=nome)
            for nome in data.exercicios
        ]

        self.session.add(plano)
        self.session.commit()
        self.session.refresh(plano)

        return plano

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────
    def update(self, id: str, data: PaymentPlansUpdateSchema):
        plano = self.get_by_id(id)

        if data.nome is not None:
            plano.nome = data.nome
        if data.preco is not None:
            plano.preco = data.preco
        if data.duracao_dias is not None:
            plano.duracao_dias = data.duracao_dias

        # Substitui todos os exercícios se vier uma nova lista
        if data.exercicios is not None:
            plano.exercicios = [
                PaymentPlanExerciseEntity(nome=nome)
                for nome in data.exercicios
            ]

        self.session.commit()
        self.session.refresh(plano)

        return plano

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────
    def delete(self, id: str):
        plano = self.get_by_id(id)

        self.session.delete(plano)
        self.session.commit()

        return {"detail": "Plano de pagamento eliminado com sucesso."}