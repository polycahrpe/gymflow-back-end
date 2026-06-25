from ..services.workout_plan_service import WorkoutPlanService
from ..schemas.workout_plan_schema import WorkoutPlanCreateSchema, WorkoutPlanUpdateSchema


class WorkoutPlanController:
    def __init__(self, session):
        self.service = WorkoutPlanService(session)

    def get_all(self):
        return self.service.get_all()

    def get_by_id(self, plan_id: str):
        return self.service.get_by_id(plan_id)

    def get_by_student(self, student_id: str):
        return self.service.get_by_student(student_id)

    def get_by_coach(self, coach_id: str):
        return self.service.get_by_coach(coach_id)

    def create(self, coach_id: str, data: WorkoutPlanCreateSchema):
        return self.service.create(coach_id, data)

    def update(self, plan_id: str, data: WorkoutPlanUpdateSchema):
        return self.service.update(plan_id, data)

    def delete(self, plan_id: str):
        return self.service.delete(plan_id)