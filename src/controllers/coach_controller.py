from ..services.coach_service import CoachService
from ..schemas.coach_schema import CoachCreateSchema, CoachUpdateSchema


class CoachController:
    def __init__(self, session):
        self.service = CoachService(session)

    def signup(self, data: CoachCreateSchema):
        return self.service.signup(data)

    def get_all(self):
        return self.service.get_all()

    def get_by_id(self, coach_id: str):
        return self.service.get_by_id(coach_id)

    def update(self, coach_id: str, data: CoachUpdateSchema):
        return self.service.update(coach_id, data)

    def activate(self, coach_id: str):
        return self.service.activate(coach_id)

    def deactivate(self, coach_id: str):
        return self.service.deactivate(coach_id)

    def delete(self, coach_id: str):
        return self.service.delete(coach_id)