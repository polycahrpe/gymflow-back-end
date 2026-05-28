from ..models.repositories.student_repository import StudentRepository
from ..schemas.student_schema import StudentCreateSchema, StudentUpdateSchema


class StudentService:
    def __init__(self, session):
        self.repo = StudentRepository(session)

    def signup(self, data: StudentCreateSchema):
        return self.repo.create(data)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, student_id: str):
        return self.repo.get_by_id(student_id)

    def get_by_coach(self, coach_id: str):
        return self.repo.get_by_coach(coach_id)

    def update(self, student_id: str, data: StudentUpdateSchema):
        return self.repo.update(student_id, data)

    def activate(self, student_id: str):
        return self.repo.activate(student_id)

    def deactivate(self, student_id: str):
        return self.repo.deactivate(student_id)

    def renovar(self, student_id: str):
        return self.repo.renovar(student_id)

    def delete(self, student_id: str):
        return self.repo.delete(student_id)