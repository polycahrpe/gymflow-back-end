from ..services.student_service import StudentService
from ..schemas.student_schema import StudentCreateSchema, StudentUpdateSchema


class StudentController:
    def __init__(self, session):
        self.service = StudentService(session)

    def signup(self, data: StudentCreateSchema):
        return self.service.signup(data)

    def get_all(self):
        return self.service.get_all()

    def get_by_id(self, student_id: str):
        return self.service.get_by_id(student_id)

    def get_by_coach(self, coach_id: str):
        return self.service.get_by_coach(coach_id)

    def update(self, student_id: str, data: StudentUpdateSchema):
        return self.service.update(student_id, data)

    def activate_by_token(self, token: str):
        return self.service.activate_by_token(token)

    def activate(self, student_id: str):
        return self.service.activate(student_id)

    def deactivate(self, student_id: str):
        return self.service.deactivate(student_id)

    def delete(self, student_id: str):
        return self.service.delete(student_id)