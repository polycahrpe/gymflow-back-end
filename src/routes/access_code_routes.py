from ..models.database.session import get_session
from .base_route import APIRouter, Depends, status
from ..controllers.access_code_controller import AccessCodeController
from ..schemas.access_code_schema import AccessCodeResponseSchema
from ..auth.dependencies import require_role


access_code_router = APIRouter(prefix="/access-codes", tags=["access-codes"])


# ADMIN — listar todos os códigos
@access_code_router.get("/all", response_model=list[AccessCodeResponseSchema])
async def get_all(
    session=Depends(get_session),
    _=Depends(require_role("admin"))
):
    controller = AccessCodeController(session)
    return controller.get_all()


# ADMIN — gerar novo código
@access_code_router.post("/generate", response_model=AccessCodeResponseSchema, status_code=status.HTTP_201_CREATED)
async def generate(
    session=Depends(get_session),
    _=Depends(require_role("admin"))
):
    controller = AccessCodeController(session)
    return controller.generate()