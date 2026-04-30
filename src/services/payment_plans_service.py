from ..models.repositories.payment_plans_repository import PaymentPlansRepository
from ..schemas.payment_plans_schema import PaymentPlansCreateSchema, PaymentPlansUpdateSchema


class PaymentPlansService:
    def __init__(self, session):
        self.repo = PaymentPlansRepository(session)

    def get_all_payment_plans(self):
        return self.repo.get_all()

    def get_payment_plan_by_id(self, plan_id: str):
        return self.repo.get_by_id(plan_id)

    def create_payment_plan(self, data: PaymentPlansCreateSchema):
        return self.repo.create(data)

    def update_payment_plan(self, plan_id: str, data: PaymentPlansUpdateSchema):
        return self.repo.update(plan_id, data)

    def delete_payment_plan(self, plan_id: str):
        return self.repo.delete(plan_id)