from ..services.payment_service import PaymentService
from ..schemas.payment_schema import PaymentCreateSchema, PaymentUpdateSchema


class PaymentController:
    def __init__(self, session):
        self.service = PaymentService(session)

    def get_all(self):
        return self.service.get_all_payments()

    def get_by_student(self, student_id: str):
        return self.service.get_payments_by_student(student_id)

    def get_by_id(self, payment_id: str):
        return self.service.get_payment_by_id(payment_id)

    def create(self, data: PaymentCreateSchema):
        return self.service.create_payment(data)

    def update(self, payment_id: str, data: PaymentUpdateSchema):
        return self.service.update_payment(payment_id, data)

    def delete(self, payment_id: str):
        return self.service.delete_payment(payment_id)