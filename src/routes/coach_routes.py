# from fastapi import APIRouter, Depends, status
from .base_route import ( APIRouter, Depends, status )
from ..models.database.session import get_session
from ..controllers.coach_controller import CoachController
from ..schemas.coach_schema import CoachCreateSchema, CoachResponseSchema
from ..auth.dependencies import require_role

coach_router = APIRouter(prefix="/coaches", tags=["coaches"])


@coach_router.post("/signup", response_model=CoachResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(data: CoachCreateSchema, session=Depends(get_session)):
    controller = CoachController(session)
    return controller.signup(data)


@coach_router.get("/all", response_model=list[CoachResponseSchema])
async def get_all(session=Depends(get_session)):
    controller = CoachController(session)
    return controller.get_all()


@coach_router.patch("/activate/{coach_id}", response_model=CoachResponseSchema)
async def activate(coach_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = CoachController(session)
    return controller.activate(coach_id)