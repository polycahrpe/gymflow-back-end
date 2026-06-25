from ..models.repositories.workout_plan_repository import WorkoutPlanRepository
from ..schemas.workout_plan_schema import WorkoutPlanCreateSchema, WorkoutPlanUpdateSchema


class WorkoutPlanService:
    def __init__(self, session):
        self.repo = WorkoutPlanRepository(session)

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, plan_id: str):
        return self.repo.get_by_id(plan_id)

    def get_by_student(self, student_id: str):
        return self.repo.get_by_student(student_id)

    def get_by_coach(self, coach_id: str):
        return self.repo.get_by_coach(coach_id)

    def create(self, coach_id: str, data: WorkoutPlanCreateSchema):
        return self.repo.create(coach_id, data)

    def update(self, plan_id: str, data: WorkoutPlanUpdateSchema):
        return self.repo.update(plan_id, data)

    def delete(self, plan_id: str):
        return self.repo.delete(plan_id)