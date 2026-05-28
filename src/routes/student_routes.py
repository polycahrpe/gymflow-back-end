from fastapi import APIRouter, Depends, status
from ..models.database.session import get_session
from ..controllers.student_controller import StudentController
from ..schemas.student_schema import (
    StudentCreateSchema,
    StudentUpdateSchema,
    StudentResponseSchema,
)
from ..auth.dependencies import require_role

student_router = APIRouter(prefix="/students", tags=["students"])


# ─────────────────────────────────────────
# PÚBLICO — signup
# ─────────────────────────────────────────
@student_router.post("/signup", response_model=StudentResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(data: StudentCreateSchema, session=Depends(get_session)):
    controller = StudentController(session)
    return controller.signup(data)


# ─────────────────────────────────────────
# ADMIN — listar todos os alunos
# ─────────────────────────────────────────
@student_router.get("/all", response_model=list[StudentResponseSchema])
async def get_all(session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.get_all()


# ─────────────────────────────────────────
# ADMIN — buscar aluno por ID
# ─────────────────────────────────────────
@student_router.get("/details/{student_id}", response_model=StudentResponseSchema)
async def get_by_id(student_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.get_by_id(student_id)


# ─────────────────────────────────────────
# ADMIN / COACH — listar alunos por coach
# ─────────────────────────────────────────
@student_router.get("/coach/{coach_id}", response_model=list[StudentResponseSchema])
async def get_by_coach(coach_id: str, session=Depends(get_session), _=Depends(require_role("admin", "coach"))):
    controller = StudentController(session)
    return controller.get_by_coach(coach_id)


# ─────────────────────────────────────────
# ADMIN — actualizar aluno
# ─────────────────────────────────────────
@student_router.put("/update/{student_id}", response_model=StudentResponseSchema)
async def update(student_id: str, data: StudentUpdateSchema, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.update(student_id, data)


# ─────────────────────────────────────────
# ADMIN — activar manualmente por ID
# ─────────────────────────────────────────
@student_router.patch("/activate/{student_id}", response_model=StudentResponseSchema)
async def activate(student_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.activate(student_id)


# ─────────────────────────────────────────
# ADMIN — desactivar conta de aluno
# ─────────────────────────────────────────
@student_router.patch("/deactivate/{student_id}", response_model=StudentResponseSchema)
async def deactivate(student_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.deactivate(student_id)


# ─────────────────────────────────────────
# ADMIN — renovar plano do aluno
# ─────────────────────────────────────────
@student_router.patch("/renovar/{student_id}", response_model=StudentResponseSchema)
async def renovar(student_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.renovar(student_id)


# ─────────────────────────────────────────
# ADMIN — apagar conta de aluno
# ─────────────────────────────────────────
@student_router.delete("/delete/{student_id}", status_code=status.HTTP_200_OK)
async def delete(student_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.delete(student_id)