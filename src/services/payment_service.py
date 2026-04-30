from ..models.repositories.payment_repository import PaymentRepository
from ..schemas.payment_schema import PaymentCreateSchema, PaymentUpdateSchema


class PaymentService:
    def __init__(self, session):
        self.repo = PaymentRepository(session)

    def get_all_payments(self):
        return self.repo.get_all()

    def get_payments_by_student(self, student_id: str):
        return self.repo.get_by_student(student_id)

    def get_payment_by_id(self, payment_id: str):
        return self.repo.get_by_id(payment_id)

    def create_payment(self, data: PaymentCreateSchema):
        return self.repo.create(data)

    def update_payment(self, payment_id: str, data: PaymentUpdateSchema):
        return self.repo.update(payment_id, data)

    def delete_payment(self, payment_id: str):
        return self.repo.delete(payment_id)