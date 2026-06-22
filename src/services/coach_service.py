from ..models.repositories.coach_repository import CoachRepository
from ..schemas.coach_schema import CoachCreateSchema, CoachUpdateSchema


class CoachService:
    def __init__(self, session):
        self.repo = CoachRepository(session)

    def signup(self, data: CoachCreateSchema):
        return self.repo.create(data)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, coach_id: str):
        return self.repo.get_by_id(coach_id)

    def update(self, coach_id: str, data: CoachUpdateSchema):
        return self.repo.update(coach_id, data)

    def activate(self, coach_id: str):
        return self.repo.activate(coach_id)

    def deactivate(self, coach_id: str):
        return self.repo.deactivate(coach_id)

    def delete(self, coach_id: str):
        return self.repo.delete(coach_id)