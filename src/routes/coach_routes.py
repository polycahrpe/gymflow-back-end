from .base_route import APIRouter, Depends, status
from ..models.database.session import get_session
from ..controllers.coach_controller import CoachController
from ..schemas.coach_schema import (
    CoachCreateSchema,
    CoachUpdateSchema,
    CoachResponseSchema,
    CoachDetailResponseSchema,
)
from ..auth.dependencies import require_role

coach_router = APIRouter(prefix="/coaches", tags=["coaches"])


# PÚBLICO — signup
@coach_router.post("/signup", response_model=CoachResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(data: CoachCreateSchema, session=Depends(get_session)):
    controller = CoachController(session)
    return controller.signup(data)


# ADMIN — listar todos os coaches
@coach_router.get("/all", response_model=list[CoachDetailResponseSchema])
async def get_all(session=Depends(get_session)):
    controller = CoachController(session)
    return controller.get_all()


# ADMIN — buscar coach por ID com alunos
@coach_router.get("/details/{coach_id}", response_model=CoachDetailResponseSchema)
async def get_by_id(coach_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = CoachController(session)
    return controller.get_by_id(coach_id)


# ADMIN — actualizar coach
@coach_router.put("/update/{coach_id}", response_model=CoachResponseSchema)
async def update(coach_id: str, data: CoachUpdateSchema, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = CoachController(session)
    return controller.update(coach_id, data)


# ADMIN — activar coach
@coach_router.patch("/activate/{coach_id}", response_model=CoachResponseSchema)
async def activate(coach_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = CoachController(session)
    return controller.activate(coach_id)


# ADMIN — desactivar coach
@coach_router.patch("/deactivate/{coach_id}", response_model=CoachResponseSchema)
async def deactivate(coach_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = CoachController(session)
    return controller.deactivate(coach_id)


# ADMIN — eliminar coach
@coach_router.delete("/delete/{coach_id}", status_code=status.HTTP_200_OK)
async def delete(coach_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = CoachController(session)
    return controller.delete(coach_id)