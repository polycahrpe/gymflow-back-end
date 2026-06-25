from ..models.database.session import get_session
from .base_route import APIRouter, Depends, status
from ..controllers.workout_plan_controller import WorkoutPlanController
from ..schemas.workout_plan_schema import (
    WorkoutPlanCreateSchema,
    WorkoutPlanUpdateSchema,
    WorkoutPlanResponseSchema,
)
from ..auth.dependencies import require_role, get_current_user


workout_plan_router = APIRouter(prefix="/workout-plans", tags=["workout-plans"])


# ADMIN/COACH — listar todas as fichas
@workout_plan_router.get("/all", response_model=list[WorkoutPlanResponseSchema])
async def get_all(
    session=Depends(get_session),
    _=Depends(require_role("admin", "coach"))
):
    controller = WorkoutPlanController(session)
    return controller.get_all()


# ADMIN/COACH/ALUNO — detalhes de uma ficha
@workout_plan_router.get("/details/{plan_id}", response_model=WorkoutPlanResponseSchema)
async def get_by_id(
    plan_id: str,
    session=Depends(get_session),
    _=Depends(require_role("admin", "coach", "student"))
):
    controller = WorkoutPlanController(session)
    return controller.get_by_id(plan_id)


# ADMIN/COACH/ALUNO — fichas de um aluno específico
@workout_plan_router.get("/student/{student_id}", response_model=list[WorkoutPlanResponseSchema])
async def get_by_student(
    student_id: str,
    session=Depends(get_session),
    _=Depends(require_role("admin", "coach", "student"))
):
    controller = WorkoutPlanController(session)
    return controller.get_by_student(student_id)


# ADMIN/COACH — fichas criadas por um coach
@workout_plan_router.get("/coach/{coach_id}", response_model=list[WorkoutPlanResponseSchema])
async def get_by_coach(
    coach_id: str,
    session=Depends(get_session),
    _=Depends(require_role("admin", "coach"))
):
    controller = WorkoutPlanController(session)
    return controller.get_by_coach(coach_id)


# COACH — criar ficha de treino
@workout_plan_router.post("/create", response_model=WorkoutPlanResponseSchema, status_code=status.HTTP_201_CREATED)
async def create(
    data: WorkoutPlanCreateSchema,
    session=Depends(get_session),
    current_user=Depends(require_role("coach"))
):
    controller = WorkoutPlanController(session)
    return controller.create(current_user.id, data)


# COACH — actualizar ficha de treino
@workout_plan_router.put("/update/{plan_id}", response_model=WorkoutPlanResponseSchema)
async def update(
    plan_id: str,
    data: WorkoutPlanUpdateSchema,
    session=Depends(get_session),
    _=Depends(require_role("coach"))
):
    controller = WorkoutPlanController(session)
    return controller.update(plan_id, data)


# COACH — apagar ficha de treino
@workout_plan_router.delete("/delete/{plan_id}", status_code=status.HTTP_200_OK)
async def delete(
    plan_id: str,
    session=Depends(get_session),
    _=Depends(require_role("coach"))
):
    controller = WorkoutPlanController(session)
    return controller.delete(plan_id)