from ..services.payment_plans_service import PaymentPlansService


class PaymentPlansController:
    def __init__(self, session):
        self.service = PaymentPlansService(session)

    def create(self, data):
        return self.service.create_payment_plan(data)

    def get_all(self):
        return self.service.get_all_payment_plans()

    def get_by_id(self, plan_id):
        return self.service.get_payment_plan_by_id(plan_id)

    def update(self, plan_id, data):
        return self.service.update_payment_plan(plan_id, data)

    def delete(self, plan_id):
        return self.service.delete_payment_plan(plan_id)