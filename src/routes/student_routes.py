from fastapi import APIRouter, Depends, status
from ..models.database.session import get_session
from ..controllers.student_controller import StudentController
from ..schemas.student_schema import StudentCreateSchema, StudentResponseSchema
from ..auth.dependencies import require_role

student_router = APIRouter(prefix="/students", tags=["students"])


# Signup público
@student_router.post("/signup", response_model=StudentResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(data: StudentCreateSchema, session=Depends(get_session)):
    controller = StudentController(session)
    return controller.signup(data)


# Listar todos — apenas admin
@student_router.get("/all", response_model=list[StudentResponseSchema])
async def get_all(session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.get_all()


# Listar alunos por coach — admin e coach
@student_router.get("/coach/{coach_id}", response_model=list[StudentResponseSchema])
async def get_by_coach(coach_id: str, session=Depends(get_session), _=Depends(require_role("admin", "coach"))):
    controller = StudentController(session)
    return controller.get_by_coach(coach_id)


# Activar aluno — apenas admin
@student_router.patch("/activate/{student_id}", response_model=StudentResponseSchema)
async def activate(student_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = StudentController(session)
    return controller.activate(student_id)